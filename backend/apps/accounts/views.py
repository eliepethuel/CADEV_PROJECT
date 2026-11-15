"""Endpoints d'authentification et de gestion du compte."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.schema import errors

from . import cookies, services, tokens
from .models import User
from .serializers import (
    AccessTokenSerializer,
    AccountSerializer,
    AuthResponseSerializer,
    DetailSerializer,
    EmailChangeConfirmSerializer,
    EmailChangeRequestSerializer,
    EmailVerifySerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordConfirmSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
)

TAG = ["Authentification"]
ACCOUNT_TAG = ["Compte"]


def _session_response(user: User, *, status_code: int = status.HTTP_200_OK) -> Response:
    """Réponse de connexion : access token dans le corps, refresh token en cookie."""
    access, refresh = tokens.issue_tokens(user)
    response = Response(
        {"access": access, "user": AccountSerializer(user).data}, status=status_code
    )
    cookies.set_refresh_cookie(response, refresh)
    return response


class PublicAuthView(APIView):
    """Vue publique sans authentification par jeton, qui répond tout de même 401."""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get_authenticate_header(self, request: Request) -> str:
        return 'Bearer realm="api"'


class RegisterView(PublicAuthView):
    throttle_scope = "register"

    @extend_schema(
        tags=TAG,
        summary="Créer un compte",
        description=(
            "Accès public. Crée un compte membre, ouvre une session (cookie de rafraîchissement "
            "`HttpOnly`) et envoie un e-mail de vérification. Le rôle n'est jamais accepté."
        ),
        request=RegisterSerializer,
        responses={201: AuthResponseSerializer, **errors(400, 429)},
    )
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.register_user(**serializer.validated_data)
        return _session_response(user, status_code=status.HTTP_201_CREATED)


class LoginView(PublicAuthView):
    throttle_scope = "login"

    @extend_schema(
        tags=TAG,
        summary="Se connecter",
        description=(
            "Accès public. Authentifie par e-mail ou nom d'utilisateur. Le refresh token est "
            "posé dans un cookie `HttpOnly` ; seul l'access token figure dans la réponse."
        ),
        request=LoginSerializer,
        responses={200: AuthResponseSerializer, **errors(400, 401, 429)},
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.authenticate_user(**serializer.validated_data)
        return _session_response(user)


class TokenRefreshView(PublicAuthView):
    # Périmètre distinct de la connexion : chaque chargement de page renouvelle la session,
    # ce qui épuiserait la limite anti-force brute et bloquerait les connexions.
    throttle_scope = "token_refresh"

    @extend_schema(
        tags=TAG,
        summary="Renouveler l'access token",
        description=(
            "Lit le refresh token dans le cookie, le révoque et en émet un nouveau (rotation). "
            "Aucun corps de requête. L'en-tête `Origin` doit être une origine autorisée."
        ),
        request=None,
        responses={200: AccessTokenSerializer, **errors(401, 403)},
    )
    def post(self, request: Request) -> Response:
        cookies.enforce_trusted_origin(request)
        access, refresh = services.rotate_refresh_token(cookies.get_refresh_cookie(request))
        response = Response({"access": access})
        cookies.set_refresh_cookie(response, refresh)
        return response


class LogoutView(PublicAuthView):
    @extend_schema(
        tags=TAG,
        summary="Se déconnecter",
        description=(
            "Révoque le refresh token du cookie et supprime ce cookie. Idempotent : répond 204 "
            "même si la session a déjà expiré."
        ),
        request=None,
        responses={204: None, **errors(403)},
    )
    def post(self, request: Request) -> Response:
        cookies.enforce_trusted_origin(request)
        tokens.blacklist_refresh_token(cookies.get_refresh_cookie(request))
        response = Response(status=status.HTTP_204_NO_CONTENT)
        cookies.clear_refresh_cookie(response)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=ACCOUNT_TAG,
        summary="Compte courant",
        description="Réservé au titulaire du compte.",
        responses={200: AccountSerializer, **errors(401)},
    )
    def get(self, request: Request) -> Response:
        return Response(AccountSerializer(request.user).data)

    @extend_schema(
        tags=ACCOUNT_TAG,
        summary="Modifier son compte",
        description=(
            "Seuls `first_name` et `last_name` sont modifiables. `role`, `is_active`, "
            "`email_verified` et `email` sont ignorés s'ils sont envoyés."
        ),
        request=AccountSerializer,
        responses={200: AccountSerializer, **errors(400, 401)},
    )
    def patch(self, request: Request) -> Response:
        serializer = AccountSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "password_reset"

    @extend_schema(
        tags=ACCOUNT_TAG,
        summary="Changer son mot de passe",
        description="Vérifie le mot de passe actuel puis ferme toutes les sessions ouvertes.",
        request=PasswordChangeSerializer,
        responses={204: None, **errors(400, 401, 429)},
    )
    def post(self, request: Request) -> Response:
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.change_password(user=request.user, **serializer.validated_data)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        cookies.clear_refresh_cookie(response)
        return response


class PasswordResetRequestView(PublicAuthView):
    throttle_scope = "password_reset"

    @extend_schema(
        tags=TAG,
        summary="Demander une réinitialisation de mot de passe",
        description=(
            "Accès public. Répond toujours 200, que l'adresse soit connue ou non, pour ne pas "
            "révéler l'existence d'un compte."
        ),
        request=PasswordResetRequestSerializer,
        responses={200: DetailSerializer, **errors(400, 429)},
    )
    def post(self, request: Request) -> Response:
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.request_password_reset(**serializer.validated_data)
        return Response(
            {"detail": "Si un compte correspond à cette adresse, un e-mail vient d'être envoyé."}
        )


class PasswordResetConfirmView(PublicAuthView):
    throttle_scope = "password_reset"

    @extend_schema(
        tags=TAG,
        summary="Confirmer la réinitialisation",
        description="Accès public avec un jeton valide à durée limitée et à usage unique.",
        request=PasswordResetConfirmSerializer,
        responses={204: None, **errors(400, 429)},
    )
    def post(self, request: Request) -> Response:
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.confirm_password_reset(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailVerifyView(PublicAuthView):
    @extend_schema(
        tags=TAG,
        summary="Vérifier son adresse e-mail",
        description="Accès public avec le jeton reçu par e-mail.",
        request=EmailVerifySerializer,
        responses={204: None, **errors(400)},
    )
    def post(self, request: Request) -> Response:
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.verify_email(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailVerifyResendView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "password_reset"

    @extend_schema(
        tags=ACCOUNT_TAG,
        summary="Renvoyer l'e-mail de vérification",
        request=None,
        responses={204: None, **errors(401, 429)},
    )
    def post(self, request: Request) -> Response:
        services.send_verification_email(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailChangeRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "password_reset"

    @extend_schema(
        tags=ACCOUNT_TAG,
        summary="Demander un changement d'adresse e-mail",
        description=(
            "L'adresse actuelle reste en vigueur tant que la nouvelle n'a pas été confirmée "
            "par le lien envoyé à celle-ci."
        ),
        request=EmailChangeRequestSerializer,
        responses={204: None, **errors(400, 401, 429)},
    )
    def post(self, request: Request) -> Response:
        serializer = EmailChangeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.request_email_change(user=request.user, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailChangeConfirmView(PublicAuthView):
    @extend_schema(
        tags=TAG,
        summary="Confirmer la nouvelle adresse e-mail",
        request=EmailChangeConfirmSerializer,
        responses={204: None, **errors(400)},
    )
    def post(self, request: Request) -> Response:
        serializer = EmailChangeConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.confirm_email_change(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=ACCOUNT_TAG,
        summary="Désactiver son compte",
        description=(
            "Désactivation logique après confirmation du mot de passe. Les sessions sont "
            "fermées ; seul un administrateur peut réactiver le compte."
        ),
        request=PasswordConfirmSerializer,
        responses={204: None, **errors(400, 401)},
    )
    def post(self, request: Request) -> Response:
        serializer = PasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.deactivate_account(user=request.user, **serializer.validated_data)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        cookies.clear_refresh_cookie(response)
        return response
