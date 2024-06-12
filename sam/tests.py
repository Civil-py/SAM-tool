from django.test import TestCase
from uuid import uuid4


# Create your tests here.

t = str(uuid4()).split('-')[3]
print(t)
#
# def add_users(request, software_id):
#     if request.method == "POST":
#         user_form = UserAllocationForm(request.POST)
#         if user_form.is_valid():
#             software = user_form.cleaned_data['software_id']
#             users = user_form.cleaned_data['users']
#
#             # Create a new UserAllocation instance and save it
#             user_allocation = UserAllocation(
#                 software_id=software,
#                 assigned=datetime.datetime.today().now(),  # Use Django's timezone utilities
#             )
#             user_allocation.save()  # Save the UserAllocation instance first
#
#             current_number_of_users = get_number_of_users(software_id)
#             # Add users to the many-to-many relationship
#             user_names = []
#             user_list = add_users_list(users, software)
#             for user in user_list:
#                 user_allocation.users.add(user)
#                 user_names.append(user)
#
#             new_number_of_users = current_number_of_users + len(user_list)
#             Software.objects.filter(software_id=software_id).update(number_of_users=new_number_of_users)
#
#             messages.success(request, f'Users {user_names} allocated to {Software.objects.get(software_id=software_id)}')
#             return redirect('software')
#     else:
#         user_form = UserAllocationForm(initial={'software_id': software_id})
#
#     return render(request, "sam/users.html", {
#         'form': user_form,
#         'software': Software.objects.get(software_id=software_id)
#     })



