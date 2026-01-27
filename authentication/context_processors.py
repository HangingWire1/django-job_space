def role_context(request):
    # This makes 'active_role' available in every HTML template automatically
    return {
        'active_page': request.session.get('active_page', 'employee')
    }