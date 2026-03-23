def create_call_reminder(customer_name, phone):

    return {
        "task": "call",
        "customer": customer_name,
        "phone": phone,
        "note": "Follow up on proposal"
    }