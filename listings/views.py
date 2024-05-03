from django.http import HttpResponse
from django.shortcuts import render, redirect

from listings.models import Band, Listing # importe le model
from listings.forms import ContactUsForm, BandForm # importe le formulaire
from django.core.mail import send_mail # pour l'envoi de mail

# Read
def show(request):
    bands = Band.objects.all() # recupère les données dans la bd qu'on stocke dans la variables bands

    return render(request, 'listings/show.html', {'bands': bands})


# show details
def show_details(request, id):

    band = Band.objects.get(id=id)
    return render(request, 'listings/show_detail.html', {'band': band}) # nous passons l'id au modèle


def band_create(request):
   form = BandForm()
   return render(request,
            'listings/band_create.html',
            {'form': form})






def about(request):
    return render(request, 'about/about.html')


def listings(request):
    listings = Listing.objects.all()

    return render(request, 'listings/listing.html', {'listings': listings})



def contact(request):
  
  # ajoutez ces instructions d'impression afin que nous puissions jeter un coup d'oeil à « request.method » et à « request.POST »
  # dans le terminal
  #print('La méthode de requête est : ', request.method)
  #print('Les données POST sont : ', request.POST)

    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@merchex.xyz'],
        )
            
        return redirect('email-sent')
        
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()



    return render(request, 'contact/contact.html', {'form': form})  # passe ce formulaire au gabarit

