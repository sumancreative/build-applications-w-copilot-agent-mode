from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    @transaction.atomic
    def handle(self, *args, **options):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create users
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel, is_superhero=True),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel, is_superhero=True),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc, is_superhero=True),
            User(name='Batman', email='batman@dc.com', team=dc, is_superhero=True),
        ]
        for user in users:
            user.save()

        # Create activities
        Activity.objects.create(user=users[0], type='Run', duration=30, date='2025-01-01')
        Activity.objects.create(user=users[1], type='Swim', duration=45, date='2025-01-02')
        Activity.objects.create(user=users[2], type='Bike', duration=60, date='2025-01-03')
        Activity.objects.create(user=users[3], type='Yoga', duration=20, date='2025-01-04')

        # Create workouts
        workout1 = Workout.objects.create(name='Super Strength', description='Strength training for superheroes')
        workout2 = Workout.objects.create(name='Agility Boost', description='Agility training for superheroes')
        workout1.suggested_for.set(users)
        workout2.suggested_for.set(users)

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, total_points=150, week='2025-W01')
        Leaderboard.objects.create(team=dc, total_points=120, week='2025-W01')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
