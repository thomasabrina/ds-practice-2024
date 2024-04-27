import socket
import sys
import os
import grpc
import logging
import uuid

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

utils_path_fraud = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path_fraud)

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books'))
sys.path.insert(0, utils_path)

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment'))
sys.path.insert(0, utils_path)

utils_path_transactionverfication = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path_transactionverfication)

utils_path_suggestions = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path_suggestions)

utils_path_order_queue = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path_order_queue)

utils_path_order_executor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path_order_executor)

from flask_cors import CORS
from utils.vector_clock import VectorClock
from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2
from utils.pb.suggestions import suggestions_pb2_grpc, suggestions_pb2
from utils.pb.books import books_pb2, books_pb2_grpc
from utils.pb.payment import payment_pb2_grpc, payment_pb2
from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

def perform_two_phase_commit(order_id, book_key, book_amount, payment_amount):
    # Prepare phase
    db_channel = grpc.insecure_channel('books-database:50055')
    payment_channel = grpc.insecure_channel('payment-system:50056')
    db_stub = books_pb2_grpc.BooksDatabaseStub(db_channel)
    payment_stub = payment_pb2_grpc.PaymentServiceStub(payment_channel)

    db_prepare = db_stub.Prepare(books_pb2.PrepareRequest(key=book_key, amount=book_amount))
    payment_prepare = payment_stub.Prepare(payment_pb2.PaymentRequest(orderId=order_id, amount=payment_amount))

    if db_prepare.success and payment_prepare.success:
        # Commit phase
        db_commit = db_stub.Commit(books_pb2.CommitRequest(key=book_key))
        payment_commit = payment_stub.Commit(payment_pb2.CommitRequest(orderId=order_id))
        return db_commit.success and payment_commit.success
    else:
        # Abort phase
        db_stub.Abort(books_pb2.AbortRequest(key=book_key))
        payment_stub.Abort(payment_pb2.AbortRequest(orderId=order_id))
        return False

def extract_order_details(request_data):
    first_item = request_data['items'][0] if 'items' in request_data and len(request_data['items']) > 0 else None
    title = first_item['name'] if first_item else None
    user_name = request_data.get('user', {}).get('name', '')
    credit_card = request_data.get('creditCard', {})
    return title, user_name, credit_card

def update_vector_clock(original_clock, response_clock):
    original_clock.merge(response_clock)
    return original_clock.get_clock()

def initialize_vector_clock():
    return VectorClock({"orchestrator": 1})

# Establish gRPC connection
def check_user_data_for_fraud(user, order_id, vector_clock):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)
        vector_clock_proto = vector_clock.to_proto(fraud_detection_pb2.VectorClock)
        
        user_data_request = fraud_detection_pb2.CheckUserDataRequest(
            orderID=order_id,
            user=fraud_detection_pb2.User(
                name=user['name'],
                contact=user.get('contact', ''),
                address=user.get('address', '')
            ),
            vector_clock=vector_clock_proto
        )
        response = stub.CheckUserDataForFraud(user_data_request)
        vector_clock.merge(VectorClock.from_proto(response.vector_clock).get_clock())
        
        return response.is_fraud, response.reason, vector_clock.get_clock()
    
def check_credit_card_for_fraud(credit_card, order_id, vector_clock):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)
        vector_clock_proto = vector_clock.to_proto(fraud_detection_pb2.VectorClock)
        
        credit_card_data_request = fraud_detection_pb2.CheckCreditCardForFraudRequest(
            orderID=order_id,
            creditCard=fraud_detection_pb2.CreditCard(
                number=credit_card['number'],
                expirationDate=credit_card['expirationDate']
            ),
            vector_clock=vector_clock_proto
        )
        response = stub.CheckCreditCardForFraud(credit_card_data_request)
        vector_clock.merge(VectorClock.from_proto(response.vector_clock).get_clock())
        
        return response.is_fraud, response.reason, vector_clock.get_clock()


def verify_credit_card_format(request_data, order_id, vector_clock):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)
        
        # Convert the VectorClock instance to the protobuf format for the gRPC call
        vector_clock_proto = vector_clock.to_proto(transaction_verification_pb2.VectorClock)
        
        # Constructing the CreditCard message
        credit_card_message = transaction_verification_pb2.CreditCard(
            number=request_data['creditCard']['number'],
            expirationDate=request_data['creditCard']['expirationDate'],
            cvv=request_data['creditCard']['cvv']
        )
        
        # Preparing the VerifyCreditCardFormatRequest
        verify_credit_card_format_request = transaction_verification_pb2.VerifyCreditCardFormatRequest(
            orderID=order_id,
            creditCard=credit_card_message,
            vector_clock=vector_clock_proto
        )
        
        # Sending the request to the TransactionVerification service
        response = stub.VerifyCreditCardFormat(verify_credit_card_format_request)
        
        # Update the vector clock with the response
        response_clock = VectorClock.from_proto(response.vector_clock)
        updated_vector_clock = vector_clock.merge(response_clock.get_clock())
        
        return response.is_valid, response.message, updated_vector_clock
    
def verify_mandatory_user_data(request_data, order_id, vector_clock):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)
        
        # Convert the VectorClock instance to the protobuf format for the gRPC call
        vector_clock_proto = vector_clock.to_proto(transaction_verification_pb2.VectorClock)
        
        # Constructing the User message
        user_message = transaction_verification_pb2.User(
            name=request_data['user']['name'],
            contact=request_data['user']['contact'],
            address=f"{request_data['billingAddress']['street']}, {request_data['billingAddress']['city']}, {request_data['billingAddress']['state']}, {request_data['billingAddress']['zip']}, {request_data['billingAddress']['country']}"
        )
        
        # Preparing the VerifyMandatoryUserDataRequest
        verify_mandatory_user_data_request = transaction_verification_pb2.VerifyMandatoryUserDataRequest(
            orderID=order_id,
            user=user_message,
            vector_clock=vector_clock_proto
        )
        
        # Sending the request to the TransactionVerification service
        response = stub.VerifyMandatoryUserData(verify_mandatory_user_data_request)
        
        # Update the vector clock with the response
        response_clock = VectorClock.from_proto(response.vector_clock)
        updated_vector_clock = vector_clock.merge(response_clock.get_clock())
        
        return response.is_valid, response.message, updated_vector_clock

def suggestions(title, author, order_id, vector_clock):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_pb2_grpc.SuggestionsStub(channel)

        # Convert the VectorClock instance to the protobuf format for the gRPC call
        vector_clock_proto = vector_clock.to_proto(suggestions_pb2.VectorClock)

        request = suggestions_pb2.SuggestionsRequest(
            orderID=order_id,
            title=title,
            author=author,
            vector_clock=vector_clock_proto
        )
        response = stub.BookSuggestions(request)

        # Update the vector clock with the response
        response_clock = VectorClock.from_proto(response.vector_clock)
        vector_clock.merge(response_clock.get_clock())
        
        # Return the list of suggested titles and the updated vector clock
        return response.titles, vector_clock.get_clock()
    
def enqueue_order(order_id, user_id, book_titles, vector_clock):
    with grpc.insecure_channel('order_queue:50054') as channel:  
        stub = order_queue_pb2_grpc.OrderQueueStub(channel)
        # Convert the VectorClock instance to the protobuf format for the gRPC call
        vector_clock_proto = vector_clock.to_proto(order_queue_pb2.VectorClock)
        
        request = order_queue_pb2.OrderRequest(
            orderId=order_id,
            userId=user_id,
            bookTitles=book_titles,
            vector_clock=vector_clock_proto  
        )
        response = stub.Enqueue(request)
        
        # Update the vector clock with the response
        response_clock = VectorClock.from_proto(response.vector_clock)
        updated_vector_clock = vector_clock.merge(response_clock.get_clock())
        
        return response.success, response.message, updated_vector_clock.get_clock()
    
def get_book_stock(key):
    with grpc.insecure_channel('books-database:50055') as channel:
        stub = books_pb2_grpc.BooksDatabaseStub(channel)
        response = stub.Read(books_pb2.ReadRequest(key=key))
        return response.value

def update_book_stock(key, amount):
    with grpc.insecure_channel('books-database:50055') as channel:
        stub = books_pb2_grpc.BooksDatabaseStub(channel)
        if amount >= 0:
            response = stub.IncrementStock(books_pb2.StockUpdateRequest(key=key, amount=amount))
        else:
            response = stub.DecrementStock(books_pb2.StockUpdateRequest(key=key, amount=-amount))
        return response.success


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)


@app.route('/checkout', methods=['POST'])
def checkout():
    
    request_data = request.json
    responses = {}
    order_id = str(uuid.uuid4())
    vector_clock = initialize_vector_clock()
    order_status = 'Order Pending'
    suggested_books = []

    # Placeholder for the previous vector clock state
    previous_vc = None

     # Event a: Verify mandatory user data
    if previous_vc is None or vector_clock.is_after(previous_vc):
        is_valid, message, vc_after_a = verify_mandatory_user_data(request_data, order_id, vector_clock)
        if not is_valid:
            return jsonify({"error": "Mandatory user data is missing", "message": message}), 400
        vector_clock = VectorClock(vc_after_a)  # Update the vector clock
    else:
        return jsonify({"error": "Event sequence error: Mandatory user data verification"}), 500
        
    # Update previous_vc for the next check
    previous_vc = vector_clock.get_clock()

    # Event b: Verify credit card format
    # Before proceeding, ensure the vector clock has advanced from the previous state
    if vector_clock.is_after(previous_vc):
        is_valid, message, vc_after_b = verify_credit_card_format(request_data, order_id, vector_clock)
        if not is_valid:
            return jsonify({"error": "Credit card format is incorrect", "message": message}), 400
        vector_clock = VectorClock(vc_after_b)  # Update the vector clock
    else:
        return jsonify({"error": "Event sequence error: Credit card format verification"}), 500

    # Update previous_vc for the next check
    previous_vc = vector_clock.get_clock()

    # Event d: Check credit card data for fraud
    if vector_clock.is_after(previous_vc):
        is_fraud, reason, vc_after_d = check_credit_card_for_fraud(request_data.get('creditCard', {}), order_id, vector_clock)
        if is_fraud:
            return jsonify({"error": "Fraud detected in credit card data", "reason": reason}), 400
        vector_clock = VectorClock(vc_after_d)  # Update the vector clock
    else:
        return jsonify({"error": "Event sequence error: Credit card data fraud check"}), 500
    previous_vc = vector_clock.get_clock()  # Update previous_vc for the next check

    # Event c: Check user data for fraud
    if vector_clock.is_after(previous_vc):
        is_fraud, reason, vc_after_c = check_user_data_for_fraud(request_data.get('user', {}), order_id, vector_clock)
        if is_fraud:
            return jsonify({"error": "Fraud detected in user data", "reason": reason}), 400
        vector_clock = VectorClock(vc_after_c)  # Update the vector clock
    else:
        return jsonify({"error": "Event sequence error: User data fraud check"}), 500
    previous_vc = vector_clock.get_clock()  # Update previous_vc for the next check

    # Event e: Generate book suggestions
    if vector_clock.is_after(previous_vc):
        title, author, _ = extract_order_details(request_data)  # Assuming extract_order_details returns title, author, and credit card
        suggested_titles, vc_after_e = suggestions(title, author, order_id, vector_clock)
        if suggested_titles:
            suggested_books = [{'title': title} for title in suggested_titles]
            order_status = 'Order Approved'
        vector_clock = VectorClock(vc_after_e)  # Update the vector clock
    else:
        return jsonify({"error": "Event sequence error: Generating book suggestions"}), 500
    previous_vc = vector_clock.get_clock()  # Update previous_vc for the next check

    # Event f: Enqueue order
    if vector_clock.is_after(previous_vc):
        book_titles = [book['title'] for book in suggested_books]
        user_id = request_data.get('user', {}).get('id', '')  # Assuming user ID is part of the request data
        success, message, vc_after_f = enqueue_order(order_id, user_id, book_titles, vector_clock)
        if not success:
            return jsonify({"error": "Failed to enqueue order", "message": message}), 400
        vector_clock = VectorClock(vc_after_f)  # Update the vector clock
        order_status = 'Order Queued'  # Update order status based on successful enqueue
    else:
        return jsonify({"error": "Event sequence error: Enqueue order"}), 500
    previous_vc = vector_clock.get_clock()  # Update previous_vc for the next check

    # Construct the response
    response = {
        'orderId': order_id,
        'status': order_status,
        'vectorClock': vector_clock.get_clock(),  # Include the final state of the vector clock
        'suggestedBooks': suggested_books if order_status == 'Order Approved' else [],
        'message': "Order processed successfully" if order_status == 'Order Approved' else "Order processing failed"
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
