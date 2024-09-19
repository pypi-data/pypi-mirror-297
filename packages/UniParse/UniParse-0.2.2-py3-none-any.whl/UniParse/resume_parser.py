import re
import spacy
from .parser import FileParser


try:
    nlp = spacy.load('en_core_web_sm')
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

# self.nlp = nlp


class ResumeParser:
    """
    A class to parse resumes and extract structured information.
    """
    
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.text = ""
        self.data = {}
        self.nlp = nlp
    
    def extract_info(self):
        """
        Extracts text from the resume file using FileParser.
        """
        parser = FileParser(self.file_path)
        self.text = parser.parse()
        if not self.text:
            raise ValueError("Failed to extract text from the resume.")
    
    def parse(self):
        """
        Parses the resume and extracts information.
        """
        self.extract_info()
        doc = self.nlp(self.text)
        self.data['name'] = self.extract_name(doc)
        self.data['email'] = self.extract_email()
        self.data['mobile_number'] = self.extract_mobile_number()
        self.data['skills'] = self.extract_skills()
        self.data['degree'] = self.extract_degree()
        self.data['college_name'] = self.extract_college()
        self.data['total_experience'] = self.extract_experience()
        self.data['is_experienced'] = bool(self.data['total_experience'])
        self.data['no_of_pages'] = self.get_number_of_pages()
        self.data['hobbies'] = self.extract_hobbies()
    
    def extract_name(self, doc):
        """
        Extracts the name from the resume using NER.
        """
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                return ent.text
        return None
    
    def extract_email(self):
        """
        Extracts email addresses using regex.
        """
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        emails = re.findall(email_pattern, self.text)
        return emails[0] if emails else None
    
    def extract_mobile_number(self):
        """
        Extracts mobile numbers using regex.
        """
        phone_pattern = r'(\+?\d{1,3}[\s-]?)?\d{10}'
        phone_numbers = re.findall(phone_pattern, self.text)
        return phone_numbers[0] if phone_numbers else None
    
    def extract_skills(self):
        """
        Extracts skills from the resume.
        """
        # Define a set of skills to look for
        skills = set(['python', 'java', 'c++', 'machine learning', 'data analysis', 'sql', 'javascript', 'excel'])
        extracted_skills = []
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', self.text, re.IGNORECASE):
                extracted_skills.append(skill)
        return extracted_skills
    
    def extract_degree(self):
        """
        Extracts degree information.
        """
        degrees = ['Bachelor', 'Master', 'B.Sc', 'M.Sc', 'B.Tech', 'M.Tech', 'PhD']
        for degree in degrees:
            if re.search(r'\b' + degree + r'\b', self.text, re.IGNORECASE):
                return degree
        return None
    
    def extract_college(self):
        """
        Extracts college or university name.
        """
        # This is a simplified example; in practice, you might use a database of college names
        college_pattern = r'University|Institute|College|School'
        matches = re.findall(college_pattern + r'.*', self.text, re.IGNORECASE)
        return matches[0] if matches else None
    
    def extract_experience(self):
        """
        Extracts total experience in years.
        """
        experience_pattern = r'(\d+)\+?\s+(years?|yrs?)\s+of\s+experience'
        matches = re.findall(experience_pattern, self.text, re.IGNORECASE)
        if matches:
            return int(matches[0][0])
        return None
    
    def get_number_of_pages(self):
        """
        Returns the number of pages in the resume.
        """
        # For simplicity, we'll assume one page per 500 words
        word_count = len(self.text.split())
        pages = word_count // 500 + 1
        return pages
    
    def extract_hobbies(self):
        """
        Extracts hobbies if mentioned.
        """
        hobby_pattern = r'Hobbies|Interests|Activities'
        if re.search(hobby_pattern, self.text, re.IGNORECASE):
            # Extract hobbies mentioned after the keyword
            hobbies_text = self.text.split(re.search(hobby_pattern, self.text, re.IGNORECASE).group())[-1]
            hobbies_list = hobbies_text.strip().split('\n')[0]
            return hobbies_list.strip()
        return None
    
    def get_extracted_data(self):
        """
        Returns the extracted data.
        """
        self.parse()
        return self.data