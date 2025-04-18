import threading


class EmailThreading(threading.Thread):
    """
    A class that extends threading.Thread to send emails in a separate thread.
    """

    def __init__(self, email_obj):
        self.email_obj = email_obj
        threading.Thread.__init__(self)

    def run(self):
        """
        The run method that sends the email.
        """
        self.email_obj.send()
