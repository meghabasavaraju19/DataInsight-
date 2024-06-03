from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import pandas as pd
from .forms import CsvForm
from .models import CSVfile
from django.conf import settings
import matplotlib.pyplot as plt
import os
import base64
import matplotlib
matplotlib.use('Agg')
from io import BytesIO

# Create your views here.

def upload_file(request):
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_detail', pk=form.instance.pk)
    else:
        form = CsvForm()
    return render(request, 'upload.html', {'form': form})

def file_list(request):
    files = CSVfile.objects.all()
    return render(request, 'file_list.html', {'files': files})

def delete_file(request, pk):
    file = get_object_or_404(CSVfile, pk=pk)
    if request.method == 'POST':
        file.delete()
        return redirect('file_list')
    return render(request, 'delete_file.html', {'file': file})

def file_detail(request, pk):
    csvfile = CSVfile.objects.get(pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, csvfile.file.name)
    df = pd.read_csv(file_path)
    
    num_columns = len(df.columns)
    columns = list(df.columns)
    descriptive_stats = df.describe().to_html()
    
    info = df.info()
    return render(request, 'file_detail.html', {
        'csv_file': csvfile,
        'num_columns': num_columns,
        'descriptive_stats': descriptive_stats,
        'columns': columns,
        'info': info,
        'pk': pk
    })

def column_detail(request, pk, colname):
    csvfile = CSVfile.objects.get(pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, csvfile.file.name)
    df = pd.read_csv(file_path)
    
    if colname not in df.columns:
        return HttpResponse('Column not found')
    
    value_count = df[colname].value_counts()
    dfvc = pd.DataFrame(value_count).reset_index()
    dfvc.columns = ['Value', 'Count']
    
    plt.figure(figsize=(10, 10))
    plt.pie(dfvc['Count'], labels=dfvc['Value'], autopct='%.2f%%')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()
    
    value_counts_items = value_count.items()
    return render(request, 'coldetail.html', {'vc': value_counts_items, 'colname': colname, 'gp': img_data})

