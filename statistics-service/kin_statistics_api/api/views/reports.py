import logging

from pydantic import ValidationError
from dependency_injector.wiring import inject, Provide
from rest_framework import status
from rest_framework.views import APIView, Request, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from api.domain.services import ManagingReportsService, UserService
from api.domain.entities import ReportPutEntity, GenerateReportEntity
from api.exceptions import ReportAccessForbidden
from api.tasks import generate_report_task
from config.containers import Container
from config.constants import DEFAULT_DATE_FORMAT
from kin_news_core.auth import JWTAuthentication


_logger = logging.getLogger(__name__)


class ReportsListView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @inject
    def get(
        self,
        request: Request,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        report_identities = reports_service.get_user_repository_names(request.user)

        return Response(
            data={'reports': [report.dict() for report in report_identities]}
        )

    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[Container.services.user_service],
    ) -> Response:
        if user_service.is_user_report_generating(request.user.id):
            return Response(status=status.HTTP_409_CONFLICT, data={'errors': 'User is generating report right now'})

        try:
            generate_report = GenerateReportEntity(
                start_date=request.data['startDate'],
                end_date=request.data['endDate'],
                channel_list=request.data['channels'],
            )

            _logger.info(f'Creating Celery job for report generation...')

            generate_report_task.delay(
                start_date=generate_report.start_date.strftime(DEFAULT_DATE_FORMAT),
                end_date=generate_report.end_date.strftime(DEFAULT_DATE_FORMAT),
                channel_list=generate_report.channel_list,
                user_id=request.user.id,
            )
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})

        return Response(status=status.HTTP_202_ACCEPTED, data={'message': 'Generating report process started successfully!'})


class ReportsSingleView(APIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @inject
    def get(
        self,
        request: Request,
        report_id: int,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        try:
            report = reports_service.get_user_detailed_report(request.user, report_id)
        except ReportAccessForbidden:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'errors': 'User does not have rights to this report!'})

        return Response(data=report.dict())

    @inject
    def put(
        self,
        request: Request,
        report_id: int,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        try:
            report_put_entity = ReportPutEntity(**request.data, report_id=report_id)
            report_identity = reports_service.set_report_name(request.user, report_put_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': str(err)})
        except ReportAccessForbidden:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'errors': 'User does not have rights to this report!'})

        return Response(data=report_identity.dict())

    @inject
    def delete(
        self,
        request: Request,
        report_id: int,
        reports_service: ManagingReportsService = Provide[Container.services.managing_reports_service],
    ) -> Response:
        try:
            reports_service.delete_report(request.user, report_id)
        except ReportAccessForbidden:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'errors': 'User does not have rights to this report!'})

        return Response(status=status.HTTP_204_NO_CONTENT)
