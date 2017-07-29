from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *

from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer

# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)


def home(request):
  return render(request, 'portfolio/home.html',
                {'portfolio': home})

@login_required
def customer_list(request):
  customer = Customer.objects.filter(created_date__lte=timezone.now())
  return render(request, 'portfolio/customer_list.html',
                {'customers': customer})

@login_required
def customer_edit(request, pk):
  customer = get_object_or_404(Customer, pk=pk)
  if request.method == "POST":
      # update
      form = CustomerForm(request.POST, instance=customer)
      if form.is_valid():
          customer = form.save(commit=False)
          customer.updated_date = timezone.now()
          customer.save()
          customer = Customer.objects.filter(created_date__lte=timezone.now())
          return render(request, 'portfolio/customer_list.html',
                        {'customers': customer})
  else:
      # edit
      form = CustomerForm(instance=customer)
  return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
  customer = get_object_or_404(Customer, pk=pk)
  customer.delete()
  return redirect('portfolio:customer_list')

@login_required
def stock_list(request):
      stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
      return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_new(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.created_date = timezone.now()
            stock.save()
            stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
            return render(request, 'portfolio/stock_list.html',
                            {'stocks': stocks})
    else:
        form = StockForm()
        # print("Else")
    return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
      stock = get_object_or_404(Stock, pk=pk)
      if request.method == "POST":
          form = StockForm(request.POST, instance=stock)
          if form.is_valid():
              stock = form.save()
              # stock.customer = stock.id
              stock.updated_date = timezone.now()
              stock.save()
              stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
              return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
      else:
          # print("else")
          form = StockForm(instance=stock)
      return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
  stock = get_object_or_404(Stock, pk=pk)
  stock.delete()
  stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
  return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def investment_list(request):
  investments = Investment.objects.filter(acquired_date__lte=timezone.now())
  return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
  if request.method == "POST":
      form = InvestmentForm(request.POST)
      if form.is_valid():
          investment = form.save(commit=False)
          investment.created_date = timezone.now()
          investment.save()
          investments = Investment.objects.filter(acquired_date__lte=timezone.now())
          return render(request, 'portfolio/investment_list.html', {'investments': investments})
  else:
      form = InvestmentForm()
      # print("Else")
  return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
  investment = get_object_or_404(Investment, pk=pk)
  if request.method == "POST":
      form = InvestmentForm(request.POST, instance=investment)
      if form.is_valid():
          investment = form.save()
          # investment.customer = investment.id
          investment.updated_date = timezone.now()
          investment.save()
          investments = Investment.objects.filter(acquired_date__lte=timezone.now())
          return render(request, 'portfolio/investment_list.html', {'investments': investments})
  else:
      # print("else")
      form = InvestmentForm(instance=investment)
  return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
  investment = get_object_or_404(Investment, pk=pk)
  investment.delete()
  investments = Investment.objects.filter(acquired_date__lte=timezone.now())
  return render(request, 'portfolio/investment_list.html', {'investments': investments})


@login_required
def fund_list(request):
  funds = Fund.objects.filter(acquired_date__lte=timezone.now())
  return render(request, 'portfolio/fund_list.html', {'fund': funds})

@login_required
def fund_new(request):
  if request.method == "POST":
      form = FundForm(request.POST)
      if form.is_valid():
          fund = form.save(commit=False)
          fund.created_date = timezone.now()
          fund.save()
          funds = Fund.objects.filter(acquired_date__lte=timezone.now())
          return render(request, 'portfolio/fund_list.html', {'funds': funds})
  else:
      form = FundForm()
      # print("Else")
  return render(request, 'portfolio/fund_new.html', {'form': form})

@login_required
def fund_edit(request, pk):
    fund = get_object_or_404(Fund, pk=pk)
    if request.method == "POST":
       form = FundForm(request.POST, instance=fund)
       if form.is_valid():
           Fund = form.save()
           # fund.customer = fund.id
           fund.updated_date = timezone.now()
           fund.save()
           funds = Fund.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/fund_list.html', {'funds': funds})
    else:
        # print("else")
        form = FundForm(instance=fund)
    return render(request, 'portfolio/fund_edit.html', {'form': form})

@login_required
def fund_delete(request, pk):
    fund = get_object_or_404(Fund, pk=pk)
    fund.delete()
    funds = Fund.objects.filter(acquired_date__lte=timezone.now())
    return render(request, 'portfolio/fund_list.html', {'funds': funds})

def portfolio(request):
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.all()
    stocks = Stock.objects.all()
    funds = Fund.objects.all()
    sum_recent_value = Investment.objects.all().aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.all().aggregate(Sum('acquired_value'))

    return render(request, 'customers/portfolio.html', {'customers': customers, 'investments': investments,
                                                        'stocks': stocks, 'funds': funds,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_acquired_value': sum_acquired_value, })


@login_required
def portfolio(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    funds = Fund.objects.filter(customer=pk)
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))

    return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                        'investments': investments,
                                                        'stocks': stocks,
                                                        'funds': funds,
                                                        'sum_recent_value': sum_recent_value,
                                                        'sum_acquired_value': sum_acquired_value, })

