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
        lines = self.text.strip().split('\n')
        
        possible_names = []
        for i in range(min(10, len(lines))):
            line = lines[i].strip()
            if line == '':
                continue
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    possible_names.append(ent.text)
            
            tokens = line.split()
            if len(tokens) >= 2 and all(token[0].isupper() for token in tokens[:2]):
                possible_names.append(line)
        
        if possible_names:
            return max(possible_names, key=len)
        else:
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
        
        from dateparser import parse
        from datetime import datetime
        
        date_patterns = [
            r'(?P<start_month>\w+)\s+(?P<start_year>\d{4})\s*[-–to]+\s*(?P<end_month>\w+)\s+(?P<end_year>\d{4}|present|Present)',
        ]
        experience_in_months = 0
        current_date = datetime.now()
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, self.text, re.IGNORECASE)
            for match in matches:
                start_month = match.group('start_month')
                start_year = match.group('start_year')
                end_month = match.group('end_month')
                end_year = match.group('end_year')
                
                start_date_str = f"{start_month} {start_year}"
                end_date_str = f"{end_month} {end_year}"
                
                start_date = parse(start_date_str)
                if end_year.lower() in ['present', 'now']:
                    end_date = current_date
                else:
                    end_date = parse(end_date_str)
                    if end_date > current_date:
                        end_date = current_date
                
                if start_date and end_date and start_date <= end_date:
                    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                    experience_in_months += months
                else:
                    continue
        
        total_experience_years = round(experience_in_months / 12, 2) if experience_in_months > 0 else None
        return total_experience_years

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