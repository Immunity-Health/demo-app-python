import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import CustomerForm
from .models import Customer


@require_http_methods(["GET", "POST"])
def customer_list(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm()

    customers = Customer.objects.order_by("-created_at")
    return render(
        request,
        "customers/customer_list.html",
        {
            "form": form,
            "customers": customers,
        },
    )


@require_http_methods(["POST"])
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect("customer_list")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def customer_api(request):
    if request.method == "GET":
        payload = [
            {
                "id": c.id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "aadhar_number": c.aadhar_number,
            }
            for c in Customer.objects.order_by("-created_at")
        ]
        return JsonResponse(payload, safe=False)

    body = json.loads(request.body.decode("utf-8"))
    customer = Customer(
        first_name=body.get("first_name", ""),
        last_name=body.get("last_name", ""),
        email=body.get("email", ""),
    )
    customer.phone = body.get("phone", "")
    customer.address = body.get("address", "")
    customer.aadhar_number = body.get("aadhar_number", "")
    customer.save()
    return JsonResponse({"id": customer.id}, status=201)
