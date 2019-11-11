from django.core.management.base import BaseCommand
from ...models import Company, Profile, Project
from django.contrib.auth.models import User
from random import randint

class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self)
        self.stdout.write('done.')

def clear_data():
    """Deletes all the table data"""
    Profile.objects.all().delete()
    Company.objects.all().delete()
    User.objects.all().delete()

def generate_companies():
    for i in range(5):
        Company(name = f'Company {i}').save()

def generate_users_with_profiles():
    for i in range(10):
        user = User(
            first_name = 'User',
            last_name = f'Number{i}',
            username = f'Username{i}',
            password = 'test'
        )
        user.save()
        user.profile.company = Company.objects.all()[int(i/2)]
        user.profile.save()

def generate_projects():
    for i in range(10):
        project = Project(
            name = f'Project {i}',
            data = [
                {
                    'year': 1,
                    'revenue': randint(0, 100)
                },
                {
                    'year': 2,
                    'revenue': randint(0, 100)
                },
                {
                    'year': 3,
                    'revenue': randint(0, 100)
                },
                {
                    'year': 4,
                    'revenue': randint(0, 100)
                }
            ],
            company = Company.objects.all()[int(i/2)]
        )
        project.save()

def run_seed(self):
    # Clear data from tables
    clear_data()

    generate_companies()
    generate_users_with_profiles()
    generate_projects()
