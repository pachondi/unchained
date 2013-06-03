# Create your views here.
from groups.models import Group
# from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
#from django.http import HttpResponse

# GET /groups
def index(request, message=""):
    group_list = Group.objects.all()
    return render_to_response(
        'groups/list.html',
        {'group_list':group_list,'message':message}
    )

# GET /groups/:id
def show(request, group_id, message=""):
    group = Group.objects.get(id=group_id)
    return render_to_response(
               'groups/form.html',                
               {
                'action':'',
                'button':'',
                'Group':group,
                'message':message
                }                   
           )

# GET /groups/new
def new(request):
    return render_to_response(
        'groups/form.html',
        {
         'action':'create',
         'button':'Create'
        }
    )

# POST /groups
def create(request):
    if request.method != "POST":
        return redirect('groups.views.new')
    
    group_name = request.POST["group_name"]
    group_description = request.POST["group_description"]
    group = Group(
                 group_name = group_name,
                 group_description = group_description      
            )
    group.save()
    return index(request,"Group Created")

#GET /groups/:id/edit
def edit(request,group_id):
    group = Group.objects.get(id=group_id)
    return render_to_response(
               'groups/form.html',                
               {
                'action':group_id + '/update',
                'button':'Update',
                'Group':group
                }                   
           )

#PUT /groups/:id
def update(request,group_id):

    group = Group.objects.get(id=group_id)
    group.group_name = request.POST["group_name"]
    group.group_description = request.POST["group_description"]
    group.save()
    return index(request,message="Group " + group.group_name + " Updated.")   
    #html = "<html><body>Testing</body></html>"
    #return HttpResponse(html)

#GET /groups/:id/delete
def delete(request,group_id):
    group = Group.objects.get(id=group_id)
    return render_to_response(
               'groups/form.html',                
               {
                'action':group_id+'/destroy',
                'button':'Delete',
                'Group':group
                }                   
           )

#DELETE /groups/:id
def destroy(request,group_id):

    if request.method != "POST":
        return redirect('groups.views.index')

    group_name = request.POST["group_name"]
    Group.objects.get(id=group_id).delete()
    return index(request,message="Group " + group_name + " Deleted.")

#def groups_home(request):
    #html = "<html><body>Testing</body></html>"
    #return HttpResponse(html)
    
"""
# GET /groups
  def index
    @groups = Group.all
  end
  
  
  # GET /groups/:id
  def show
    #@groups = Group.where("user_id = ?",current_user.id)
    @group = Group.find(params[:id])
  end

  # GET /groups/new
  def new
    @group = Group.new
  end
  
  # POST /groups
  def create
    params[:group].merge!("user_id" => @current_user.id)
    @group = Group.new(params[:group])
    if @group.save
      flash[:notice] = "Group created! #{params} #{params[:group]}"
      redirect_back_or_default groups_path
    else
      render :action => :new
    end
  end
  
  #GET /groups/:id/edit
  def edit
    @group = Group.find(params[:id])
  end  
  
  #PUT /groups/:id
  def update
    @group = Group.find(params[:id])
    
    if @group.update_attributes(params[:group])
      flash[:notice] = "Group was successfully updated #{params}"
      respond_with @group, :location => groups_path
    end
    # rails 2 way
    #respond_to do |format|
      #if @group.update_attributes(params[:group])
        #format.html { redirect_to @group, notice:'Group was successfully updated'}
      #else
        #format.html { render action:"edit", notice:'Group was unsuccessfully updated'}
      #end
    #end 
  
  end
  
  #DELETE /groups/:id
  def destroy
    #Can only deactivate if the group was created by the owner
    #should only deactivate and not delete the group.  
    Group.find(params[:id]).destroy
    flash[:notice] = "Group Deleted!"
    redirect_back_or_default groups_path
  end
  """