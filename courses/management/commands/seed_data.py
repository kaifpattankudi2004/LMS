from django.core.management.base import BaseCommand
from courses.models import Course, Lesson

class Command(BaseCommand):
    help = 'Seed the database with initial courses and lessons'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Course.objects.all().delete()

        courses_data = [
            {
                'title': 'Python for Beginners',
                'description': 'Learn the basics of Python programming from scratch. This course covers variables, loops, functions, and basic data structures.',
                'thumbnail': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800',
                'category': 'Programming',
                'lessons': [
                    {'title': 'Python for Beginners', 'url': 'https://www.youtube.com/embed/kqtD5dpn9C8', 'order': 1},
                    {'title': 'Python Variables & Types', 'url': 'https://www.youtube.com/embed/_uQrJ0TkZlc', 'order': 2},
                    {'title': 'Python Full Course', 'url': 'https://www.youtube.com/embed/rfscVS0vtbw', 'order': 3},
                ]
            },
            {
                'title': 'Modern Web Development',
                'description': 'Master the fundamentals of HTML, CSS, and JavaScript to build beautiful and responsive websites.',
                'thumbnail': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800',
                'category': 'Web Development',
                'lessons': [
                    {'title': 'HTML Crash Course', 'url': 'https://www.youtube.com/embed/qz0aGYrrlhU', 'order': 1},
                    {'title': 'CSS for Beginners', 'url': 'https://www.youtube.com/embed/1Rs2ND1ryYc', 'order': 2},
                    {'title': 'JavaScript Tutorial', 'url': 'https://www.youtube.com/embed/W6NZfCO5SIk', 'order': 3},
                ]
            },
            {
                'title': 'Data Science with Python',
                'description': 'Dive into data analysis using Pandas, NumPy, and Matplotlib. Perfect for aspiring data scientists.',
                'thumbnail': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
                'category': 'Data Science',
                'lessons': [
                    {'title': 'Pandas for Data Science', 'url': 'https://www.youtube.com/embed/vmEHCJofslg', 'order': 1},
                    {'title': 'NumPy Explained', 'url': 'https://www.youtube.com/embed/QUT1VHiLmmI', 'order': 2},
                    {'title': 'Data Analysis Tutorial', 'url': 'https://www.youtube.com/embed/r-uOLxNrNk8', 'order': 3},
                ]
            },
            {
                'title': 'React.js Masterclass',
                'description': 'Build powerful frontend applications with React. Learn hooks, state management, and component architecture.',
                'thumbnail': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800',
                'category': 'Web Development',
                'lessons': [
                    {'title': 'React Tutorial for Beginners', 'url': 'https://www.youtube.com/embed/SqcY0GlETPk', 'order': 1},
                ]
            },
            {
                'title': 'Node.js Backend Essentials',
                'description': 'Master backend development with Node.js and Express. Build scalable APIs and handle database integrations.',
                'thumbnail': 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=800',
                'category': 'Programming',
                'lessons': [
                    {'title': 'Node.js Tutorial for Beginners', 'url': 'https://www.youtube.com/embed/TlB_eWDSMt4', 'order': 1},
                ]
            },
            {
                'title': 'Machine Learning Fundamentals',
                'description': 'Start your journey into AI. Learn regression, classification, and clustering with real-world datasets.',
                'thumbnail': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800',
                'category': 'Artificial Intelligence',
                'lessons': [
                    {'title': 'Machine Learning for Beginners', 'url': 'https://www.youtube.com/embed/gmvvaobm7eQ', 'order': 1},
                ]
            },
            {
                'title': 'UI/UX Design Principles',
                'description': 'Learn to design beautiful and user-friendly interfaces. Master Figma, wireframing, and prototyping.',
                'thumbnail': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800',
                'category': 'Design',
                'lessons': [
                    {'title': 'UI/UX Design Full Course', 'url': 'https://www.youtube.com/embed/ODpB9-MCa5s', 'order': 1},
                ]
            },
            {
                'title': 'Digital Marketing Mastery',
                'description': 'Grow brands online. Master SEO, Social Media Marketing, and Google Ads strategies.',
                'thumbnail': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800',
                'category': 'Marketing',
                'lessons': [
                    {'title': 'Digital Marketing Full Course', 'url': 'https://www.youtube.com/embed/dS0PtshQDls', 'order': 1},
                ]
            },
            {
                'title': 'Cybersecurity Essentials',
                'description': 'Protect systems from cyber threats. Learn network security, ethical hacking, and risk management.',
                'thumbnail': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800',
                'category': 'IT Security',
                'lessons': [
                    {'title': 'Cyber Security Full Course', 'url': 'https://www.youtube.com/embed/inWWhr5tnEA', 'order': 1},
                ]
            },
            {
                'title': 'AWS Cloud Practitioner',
                'description': 'Master Amazon Web Services. Learn about EC2, S3, IAM, and cloud architecture best practices.',
                'thumbnail': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800',
                'category': 'Cloud Computing',
                'lessons': [
                    {'title': 'AWS Tutorial for Beginners', 'url': 'https://www.youtube.com/embed/k1RI5locZE4', 'order': 1},
                ]
            },
            {
                'title': 'Mobile Apps with Flutter',
                'description': 'Build cross-platform mobile apps for iOS and Android using a single codebase and Dart.',
                'thumbnail': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800',
                'category': 'Mobile Development',
                'lessons': [
                    {'title': 'Flutter Tutorial for Beginners', 'url': 'https://www.youtube.com/embed/1ukSR1GRtMU', 'order': 1},
                ]
            },
            {
                'title': 'SQL & Database Design',
                'description': 'Master relational databases. Learn to write complex queries, joins, and optimize database performance.',
                'thumbnail': 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=800',
                'category': 'Programming',
                'lessons': [
                    {'title': 'SQL Tutorial for Beginners', 'url': 'https://www.youtube.com/embed/HXV3zeQKqGY', 'order': 1},
                ]
            },
            {
                'title': 'DevOps Engineering Roadmap',
                'description': 'Learn the tools of modern software delivery. Master Docker, Kubernetes, Jenkins, and CI/CD.',
                'thumbnail': 'https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800',
                'category': 'DevOps',
                'lessons': [
                    {'title': 'DevOps Full Course', 'url': 'https://www.youtube.com/embed/Xrgk023l4lI', 'order': 1},
                ]
            },
            {
                'title': 'Git & GitHub Mastery',
                'description': 'Master version control. Learn branching, merging, pull requests, and collaborative workflow.',
                'thumbnail': 'https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800',
                'category': 'Programming',
                'lessons': [
                    {'title': 'Git Tutorial for Beginners', 'url': 'https://www.youtube.com/embed/RGOj5yH7evk', 'order': 1},
                ]
            },
            {
                'title': 'Full Stack MERN',
                'description': 'Build a complete social media app from scratch using MongoDB, Express, React, and Node.js.',
                'thumbnail': 'https://images.unsplash.com/photo-1633356122102-3fe601e05bd2?w=800',
                'category': 'Web Development',
                'lessons': [
                    {'title': 'MERN Stack Full Course', 'url': 'https://www.youtube.com/embed/F9gB5b4jgOI', 'order': 1},
                ]
            }
        ]

        for c_data in courses_data:
            lessons_data = c_data.pop('lessons')
            course = Course.objects.create(**c_data)
            for l_data in lessons_data:
                Lesson.objects.create(course=course, title=l_data['title'], youtube_url=l_data['url'], order=l_data['order'])
            self.stdout.write(self.style.SUCCESS(f'Successfully created course: {course.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
