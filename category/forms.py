from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['category_name','description','cat_image']

    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)

        self.fields['category_name'].widget.attrs['placeholder']='Enter Category name'
        self.fields['category_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['category_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Category discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3
        
        self.fields['cat_image'].widget.attrs['placeholder']='Add images'
        self.fields['cat_image'].widget.attrs['class']='form-control'
        self.fields['cat_image'].widget.attrs['type']='file'