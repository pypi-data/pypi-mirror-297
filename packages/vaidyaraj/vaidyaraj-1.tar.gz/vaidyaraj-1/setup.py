from setuptools import setup, find_packages
import os

VERSION = '1'
DESCRIPTION = '''
Introducing Vaidyanath: The Future of Holistic Health Assistance! 🌿💥

Get ready to revolutionize your well-being with Vaidyanath, the ultimate AI-powered health assistant blending the wisdom of Ayurveda, homeopathy, and modern medicine! Whether you're seeking personalized health tips, stress relief, or lifestyle advice, Vaidyanath has you covered—complete with Sanskrit shloks and immersive soundscapes.

Say goodbye to traditional health apps and hello to a truly holistic experience. Vaidyanath isn't just advice—it's a wellness journey.

🌟 Experience the future of healthcare, today! 🌟
'''

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="vaidyaraj",
    version=VERSION,
    author="Suraj Sharma",
    author_email="Surajsharma963472@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,  # Set the long description
    long_description_content_type="text/markdown",  # Specify that the long description is in Markdown format
    packages=find_packages(),
    install_requires=[
        'pathlib'
        'edge_tts',
        'pygame',
        'groq'
    ],
    keywords=['Surya', 'Vaidya', 'Vaidyanath', 'python tutorial', 'Suraj', 'Doctor', 'groq'],
)
