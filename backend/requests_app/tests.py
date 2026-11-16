from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from requests_app.models import Category, ServiceRequest

User = get_user_model()

class ServiceRequestValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="labuser", password="password123")
        self.category = Category.objects.create(name="Hardware Support")

    def test_resolved_request_requires_resolution_fields(self):
        # Attempt to create a resolved request without resolved_at or resolution_summary
        req = ServiceRequest(
            requester=self.user,
            category=self.category,
            title="Broken Projector",
            description="Bulb blew out in conference room",
            location="Room 402",
            status=ServiceRequest.Status.RESOLVED
        )
        
        # full_clean() should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            req.full_clean()
            
        # Verify specific errors are flagged
        self.assertIn("resolved_at", context.exception.error_dict)
        self.assertIn("resolution_summary", context.exception.error_dict)

    def test_valid_resolved_request_passes(self):
        # Create a valid resolved request with all required fields
        req = ServiceRequest(
            requester=self.user,
            category=self.category,
            title="Fixed Projector",
            description="Bulb blew out in conference room",
            location="Room 402",
            status=ServiceRequest.Status.RESOLVED,
            resolved_at=timezone.now(),
            resolution_summary="Replaced the projector bulb with a spare unit."
        )
        
        # Should not raise any validation error
        try:
            req.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly for valid resolved request.")