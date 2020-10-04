SERVER_TYPE_SYSTEM_SERVER = 1
SERVER_TYPE_USER_SERVER = 2
SERVER_TYPE_CHOICES = (
    (SERVER_TYPE_SYSTEM_SERVER, 'System Server'),
    (SERVER_TYPE_USER_SERVER, 'User Server')
)

# Bootstrap CSS classes for device/rack statuses
SERVER_TYPE_CLASSES = {
    1: 'success',
    2: 'danger',
}
