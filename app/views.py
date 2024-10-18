from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import pandas as pd

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        try:
            if filename.endswith('.csv'):
                encodings = ['utf-8', 'iso-8859-1', 'latin1', 'cp1252']
                for encoding in encodings:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("Unable to decode the CSV file with any of the attempted encodings.")
            else:  
                df = pd.read_excel(file_path)
            
            
            summary = generate_summary(df)
            
        
            request.session['summary'] = summary
            
            return redirect('summary')
        except Exception as e:
            
            print(f"Error processing file: {str(e)}")
            return render(request, 'app/upload.html', {'error': str(e)})
    
    return render(request, 'app/upload.html')

def summary(request):
    
    summary = request.session.get('summary', None)
    
    if summary is None:
        return render(request, 'app/summary.html', {'error': 'No summary available.'})
    
    return render(request, 'app/summary.html', {'summary': summary})

def generate_summary(df):
    """
    Generates a summary for the uploaded file. 
    This is just an example; you can customize this based on your requirement.
    """
    summary = df.describe(include='all').to_string()
    return summary
