document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var messages = document.getElementById('messages');
        if (messages) {
            messages.style.display = 'none';
        }
    }, 3000); // 3000 milliseconds = 3 seconds
});