from plyer import notification

def show_notification(title, message):
    # Display the notification
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Time in seconds for the notification to stay visible
    )

# Example usage:

