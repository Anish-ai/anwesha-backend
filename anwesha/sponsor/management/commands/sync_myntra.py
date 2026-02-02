from django.core.management.base import BaseCommand
from sponsor.models import MyntraRegistration
from user.models import User
import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
import json
import os


class Command(BaseCommand):
    help = 'Sync Myntra registrations from Google Sheets'

    def handle(self, *args, **options):
        try:
            # Get Google Sheets credentials from Secret Manager
            # In production, this is stored in Secret Manager
            creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
            
            if not creds_json:
                self.stdout.write(self.style.ERROR('GOOGLE_SHEETS_CREDENTIALS not found in environment'))
                return
            
            # Parse credentials
            creds_dict = json.loads(creds_json)
            creds = Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            
            # Connect to Google Sheets
            client = gspread.authorize(creds)
            sheet_id = '1HsKe7rPy6dK3kwRepgq0sPC-cFodo24bzN6Sc0ySQrc'
            sheet = client.open_by_key(sheet_id)
            worksheet = sheet.get_worksheet(0)  # First sheet
            
            # Get all values
            records = worksheet.get_all_records()
            
            self.stdout.write(f'Found {len(records)} records in Google Sheets')
            
            created_count = 0
            updated_count = 0
            not_found_count = 0
            
            # Email column name from sheet
            email_column = 'Email ID'
            
            for record in records:
                email = record.get(email_column, '').strip()
                
                if not email:
                    continue
                
                # Try to find user by email
                try:
                    user = User.objects.get(email__iexact=email)
                    anwesha_user_id = user.anwesha_id
                except User.DoesNotExist:
                    anwesha_user_id = None
                    not_found_count += 1
                
                # Create or update Myntra registration
                myntra_reg, created = MyntraRegistration.objects.update_or_create(
                    email=email,
                    defaults={
                        'anwesha_user_id': anwesha_user_id,
                        'raw_data': record,
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            self.stdout.write(self.style.SUCCESS(
                f'Sync complete:\n'
                f'  Created: {created_count}\n'
                f'  Updated: {updated_count}\n'
                f'  Users not found: {not_found_count}'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during sync: {str(e)}'))
            import traceback
            traceback.print_exc()
