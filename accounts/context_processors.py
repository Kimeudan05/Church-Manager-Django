def role_context(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            return {
                "role": profile.role,
                "user_profile": profile,
                "user_group": profile.group,
            }
        except:
            return {"role": None, "user_profile": None, "user_group": None}
    return {"role": None, "user_profile": None, "user_group": None}
