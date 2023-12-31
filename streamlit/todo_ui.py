import streamlit as st
import requests
import json
import pandas as pd
from streamlit_option_menu import option_menu


st.set_page_config(layout="wide")

local_host = 'http://localhost:8000/'

session_state = st.session_state

def get_jwt_token(username, password):
    
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
    

def get_data(token):

    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return token
    else:
        return None

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:

    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ8NDQ0NFREWFhURFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDQ0NFRAPFS0dFR0rKy0rLSsrLSstLSstLS0tKysrKystLS0rKystKy0rKystLSstKy0rLSstLTctLS03K//AABEIAK4BIgMBIgACEQEDEQH/xAAWAAEBAQAAAAAAAAAAAAAAAAAAAQf/xAAYEAEBAQEBAAAAAAAAAAAAAAAAARExEv/EABgBAQEBAQEAAAAAAAAAAAAAAAABAgYF/8QAHBEBAQEAAgMBAAAAAAAAAAAAAAERMVESIUFx/9oADAMBAAIRAxEAPwDUwHHvSAAAUEUGpE0AKAAAAAChIKi/iACKAAAIAICgIAAIKgoBhIgAigAAAAACgqFAW1AAUAUAAAFQAAAAAAFDPQgCKAIAAAEJNDEtVEt6ABFAAAAFRVQAAAUAFAFEEVGrMAUQQUUQUBFCmQEBKACAAKAIACAioAAigAALxZELAAAAAFABRQlRrekFRUABQAAAAAARRBBUABUxUAQAAEVEACIoL5ovjU0EU0AAAFAAABQBVAQEUBQFgvwQBAAAQEAFxcAoiWgAyoAgIqAAIq6IL5VMFRRQBUAFAVFsxABFAAFQVFCFWC6iBuigAICAAAAigAACAAgIoCAIAAoqKqACgpqNccIAIoAAAAAAAqAAKgAAoIAigAACABABRrhEAZUAQAFARUARVABQAAAAAMAAAAAAAFIgILoAIoAAAgKgsFQFABAAQAABai2YgAKAAAALhCtZ9QQVORFAwAAAFwADARRMEFDBBUMAwEwADAAFAEABcRcQF2dHsAZUAUAAAFQAAABRAFEVQEEFEAUQABQRQXhEARQBAAFAAWoBbqACKAAAABBQAQAFAAAAiKJotvwAEUAAAAVA0AAAAAEAAAAAAAAH/9k=");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


    col1,col2,col3=st.columns(3)
    
    with col2:
        col1,col2=st.columns([1,2])
        
        with col1:
            todo_logo="https://icon-library.com/images/todo-icon/todo-icon-5.jpg"
            st.image(todo_logo, caption="", width=170)

        with col2:
            st.header('TODO APP')

    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 ,col3= st.columns(3)
        with col2:
            login_button = st.button("Login")

    if login_button:
        token = get_jwt_token(username, password)
        
        if token:
            data = get_data(token)
            
            if data:
                st.session_state['logged_in'] = True
                st.session_state['token'] = token
                st.session_state['username']=username
                st.experimental_rerun()
            else:
                 st.write("You do not have permission to access the next page")

        else:
            st.error("Invalid username or password.")

if 'logged_in' in st.session_state and st.session_state['logged_in']:

    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://slidescorner.com/wp-content/uploads/2023/03/03-Baby-Blue-Pastel-Plain-Background-Wallpaper-by-SlidesCorner.com_-1-500x281.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

    token=st.session_state['token']
    username=st.session_state['username']

    col3,col4=st.columns([8,2])

    with col3:
        selected=option_menu(menu_title="Menu",
            options=["To-Do","History"],
            menu_icon="cast",
            icons=["card-checklist","h-square"],
            orientation="horizontal",)

        if selected=="To-Do":

            col1,col2=st.columns(2)

            with col1:
                with st.form(key="adddtask_form",clear_on_submit=True):
                    task=st.text_input("Task")
                    add_button=st.form_submit_button("Add Task")
                if task:
                    task_data={
                        "task":task
                    }
                    url=local_host+'todo/?type=savetask'
                    headers = {'Authorization': f'Bearer {token}'}
                    response=requests.post(url,headers=headers,params=task_data)

                record_data={
                    "username":username,
                    "task":task,
                    "description":"",
                    "status":"pending",
                }
                if add_button:
                    
                    url=local_host+'todo/?type=insert'
                    headers = {'Authorization': f'Bearer {token}'}
                    response=requests.post(url,headers=headers,params=record_data)
                    if response.status_code==200:
                        st.write("Task added successfully")
                    
            with col2:

                url=local_host+'todo/?type=fetch_pending'
                headers = {'Authorization': f'Bearer {token}'}
                params={
                    "username":username
                }
                response=requests.get(url,headers=headers,params=params)
                if response.status_code==200:
                    record=response.json()
                    task=record['tasklist']
                    for item in range(len(task)):
                        task_button=st.checkbox(task[item],key=f'{item}{task[item]}')
                        if task_button:
                            update_button=st.radio("Complete or Delete",("Complete task","Delete task"),key=f'{item}')
                            if update_button=='Complete task':
                                with st.container():
                                    with st.form(key=f"update_form.{item}",clear_on_submit=True):
                                        description = st.text_area("Description")
                                        file=st.file_uploader("please choose a file")
                                        submit = st.form_submit_button("submit")
                                        if description:
                                            if submit:
                                                url=local_host+'todo/?type=update'
                                                headers = {'Authorization': f'Bearer {token}'}
                                                params={
                                                    "username":username,
                                                    "task":task[item],
                                                    "description":description,
                                                    "status":"done",
                                                }
                                                files={
                                                    'file':file
                                                }
                                                update_response=requests.post(url,headers=headers,params=params,files=files)
                                                if update_response.status_code==200:
                                                    update_message=update_response.json()
                                                    st.write(update_message)
                                                    st.write(update_message['message'])
                                                    st.experimental_rerun()
                            elif update_button=='Delete task':
                                
                                url=local_host+'todo/?type=delete'
                                headers = {'Authorization': f'Bearer {token}'}
                                params={
                                    "username":username,
                                    "task":task[item],
                                }
                                response=requests.post(url,headers=headers,params=params)
                                if response.status_code==200:
                                    delete_message=response.json()
                                    st.write(delete_message['message'])
                                    st.experimental_rerun()
            
                else:
                    st.error("Unable to fetch the data")


        if selected=="History":
            col1,col2=st.columns(2)

            with col1:
                url=local_host+'todo/?type=fetch_total'
                headers = {'Authorization': f'Bearer {token}'}
                params={
                    "username":username
                }
                response=requests.get(url,headers=headers,params=params)
                if response.status_code==200:
                    task_history=response.json()
                    st.header("Total Tasks")
                    df = pd.DataFrame(task_history)
                    df.index = [i+1 for i in range(len(df))]
                    df.index.name = 'S.No'
                    st.dataframe(df, height=None)

            with col2:
                params={
                    "username":username,
                }     
            
                url = local_host + "todo/?type=fetch_done"
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(url,headers=headers,params=params)
                
                if response.status_code == 200:
                    record = response.json()
                    tasks = record['tasks']
                    files = record['files']
                    description = record['description']
                    st.header("Completed Tasks")
                    for i in range(len(tasks)):
                        done_task = st.button(f'{i+1}.{tasks[i]}')
                        button_style = """
                            <style>
                            .stButton>button {
                                background: none;
                                border: none;
                                padding: 0;
                                margin: 0;
                                font-size: inherit;
                                font-family: inherit;
                                cursor: pointer;
                                outline: inherit;
                            }
                            </style>
                        """
                        st.markdown(button_style, unsafe_allow_html=True)
                        if done_task:
                            st.write("Description:", description[i])                        
                            st.write("Click the link to download the file:", files[i])         
                else:
                    st.error("Unable to fetch the data")  

    with col4:
        profile_photo="https://media.istockphoto.com/id/1337144146/vector/default-avatar-profile-icon-vector.jpg?s=612x612&w=0&k=20&c=BIbFwuv7FxTWvh5S3vB6bkT0Qv8Vn8N5Ffseq84ClGI="
        st.image(profile_photo,width=350)
        st.markdown(f"<h1 style='text-align: center; '>{username}</h1> <br>", unsafe_allow_html=True)
