document.getElementById('uploadButton').addEventListener('click', function()
{
    this.disabled = true;
    this.form.submit();
    
}
);