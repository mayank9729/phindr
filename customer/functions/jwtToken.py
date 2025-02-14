from rest_framework_simplejwt.tokens import RefreshToken
def jwtToken(customer):
    try:
        refresh = RefreshToken.for_user(customer)
        refresh['email'] = customer.email   
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    except Exception as e:
        return {"error": str(e)}
