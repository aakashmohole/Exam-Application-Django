from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):
    feedbacks = CustomerFeedback.objects.all()
    return render(request, 'surveys.html', {"feedbacks": feedbacks})


def customer_feedback(request, id):
    feedback = CustomerFeedback.objects.get(id=id)
    
    if request.method == "POST":
        for question in feedback.questions.all():
            
            response_text = request.POST.get(f"response_{question.id}")
            selected_option_ids = request.POST.getlist(f"options_{question.id}")
            
            response = CustomerResponse.objects.create(
                feedback=feedback,
                question=question,
                response_text=response_text if question.question_type in ["Text", "BigText"] else None
            )

            # If options are selected, link them to the response
            if selected_option_ids:
                # Correct query: Use `id` to filter by the correct option IDs
                selected_options = Options.objects.filter(id__in=selected_option_ids)
                print(selected_options)  # Debugging output
                response.selected_options.set(selected_options)  # Set the selected options
                
            response.save()  # Don't forget to save the response object with the selected options

        return redirect("/thank-you/")
    
    return render(request, 'survey.html', {"questions": feedback.questions.all()})


def thank_you(request):
    return render(request, "thank-you.html")