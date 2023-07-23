from django.shortcuts import render

def terms_and_conditions(request):
    return render(request, 'legal/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')

def learning_resources(request):
    resources = [
        'Glossary of Stock Market Terms',
        'Practice Your Skills with MarketWatch Virtual Game',
        'Get Free Stocks with My Webull Referral Code',
        '9 Expert-Recommended Educational Resources For Newcomers To The Stock Market',
        'The Best Online Stock Trading Classes of 2023',
        '10 Great Ways to Learn Stock Trading in 2023',
        # Add more resources as needed
    ]
    return render(request, 'learning_resources.html', {'resources': resources})
