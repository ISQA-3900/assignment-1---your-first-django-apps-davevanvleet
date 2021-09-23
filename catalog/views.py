from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
def Email(request):
    subject = "this can be a form field value or user info the email subject"
    message = "this can be a form field value or user info the email subject"
    user = request.user  #request was passed to the method as a parameter for the view
    user_email = user.email # pull user’s email out of the user record#try to send the e-mail – note you can send to multiple users – this just sends#to one user.
    try:    
        send_mail(subject, message, 'davevvwebapp@gmail.com', [user_email])    
        sent = True
    except:    
        print("Error sending e-mail")

    return render(request, "password_reset_email.html")
    
