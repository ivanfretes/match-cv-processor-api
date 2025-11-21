"""Text cleaner adapter - Implements TextCleanerPort"""
import re
from domain.ports.text_cleaner_port import TextCleanerPort


class TextCleanerAdapter(TextCleanerPort):
    """Adapter for text cleaning and normalization"""
    
    def clean(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned and normalized text
        """
        if not text:
            return ""
        
        # Remove control and non-printable characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Replace tabs with spaces
        text = text.replace('\t', ' ')
        
        # Split into lines first
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return ""
        
        # Process lines: join short lines (loose words) and preserve structure
        cleaned_lines = []
        prev_was_short = False
        
        for line in lines:
            is_short = len(line) < 60  # Short line (probably loose word)
            is_very_short = len(line) < 30
            ends_sentence = bool(re.search(r'[.!?]\s*$', line))
            is_title_caps = bool(re.match(r'^[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{3,}$', line) and len(line) < 50)
            
            # If it's a very short line, probably a loose word - join with previous
            if is_very_short and cleaned_lines and not ends_sentence:
                if cleaned_lines:
                    cleaned_lines[-1] = cleaned_lines[-1] + ' ' + line
                else:
                    cleaned_lines.append(line)
            # If short but previous was also short and doesn't end in sentence, join
            elif is_short and cleaned_lines and prev_was_short and not ends_sentence:
                cleaned_lines[-1] = cleaned_lines[-1] + ' ' + line
            # If it's a title in caps, keep it as new line
            elif is_title_caps:
                if cleaned_lines:
                    cleaned_lines.append('')  # Empty line before title
                cleaned_lines.append(line)
            # If previous line ended in sentence and this starts with capital, new line
            elif cleaned_lines and re.search(r'[.!?]\s*$', cleaned_lines[-1]) and re.match(r'^[A-ZÁÉÍÓÚÑ]', line):
                cleaned_lines.append(line)
            # If line is very long (complete paragraph), keep it separated
            elif len(line) > 120:
                if cleaned_lines:
                    cleaned_lines.append('')
                cleaned_lines.append(line)
            # By default, join with previous if both are short
            elif is_short and cleaned_lines and len(cleaned_lines[-1]) < 100:
                cleaned_lines[-1] = cleaned_lines[-1] + ' ' + line
            else:
                # New line
                cleaned_lines.append(line)
            
            prev_was_short = is_short or is_very_short
        
        # Join all lines
        text = '\n'.join(cleaned_lines)
        
        # Clean multiple spaces within each line
        lines = text.split('\n')
        lines = [re.sub(r' +', ' ', line.strip()) for line in lines]
        text = '\n'.join(lines)
        
        # Normalize spaces around punctuation
        # Remove spaces before punctuation
        text = re.sub(r' +([.,:;!?])', r'\1', text)
        # Add space after punctuation if missing
        text = re.sub(r'([.,:;!?])([^\s\n])', r'\1 \2', text)
        
        # Remove empty lines at start and end
        lines = [line for line in text.split('\n')]
        # Remove empty lines at start
        while lines and not lines[0].strip():
            lines.pop(0)
        # Remove empty lines at end
        while lines and not lines[-1].strip():
            lines.pop()
        
        text = '\n'.join(lines)
        
        # Reduce multiple consecutive line breaks to max 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Clean spaces at start and end of complete text
        text = text.strip()
        
        return text

