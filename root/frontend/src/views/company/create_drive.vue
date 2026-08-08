<template>

<h2>Create Placement Drive</h2>

<form @submit.prevent="createDrive">

<label>Job Title</label>
<input type="text" placeholder="Job Title" v-model="form.job_title" required>
<br><br>

<label>Description</label>
<textarea placeholder="Description" v-model="form.description" required></textarea>
<br><br>

<label>Required Courses </label>
<input type="text" placeholder="Course" v-model="form.course" required>
<br><br>

<label>Required Minimum CGPA </label>
<input type="number" step="0.01" placeholder="Minimum CGPA" v-model="form.min_cgpa" required>
<br><br>

<label>Required Graduation Year</label>
<input type="number" placeholder="Graduation Year" v-model="form.graduation_year" required >
<br><br>

<label>Offering Salary</label>
<input type="number" placeholder="Salary" v-model="form.salary" required>
<br><br>

<label>Application Deadline</label>
<input type="date" v-model="form.application_deadline" required>
<br><br>

<button type="submit">Create Drive</button>
<button type="button" @click="$router.back()">Cancel</button>

</form>

<p>{{ message }}</p>

</template>

<script>

export default{

    data(){

        return{
            form:{
                job_title:"",
                description:"",
                course:"",
                min_cgpa:"",
                graduation_year:"",
                salary:"",
                application_deadline:""
            },
            message:""
        }

    },

    methods:{

        async createDrive(){

            let response=await fetch(
                "http://127.0.0.1:5000/company/create_drive",
                {
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    },
                    body:JSON.stringify(this.form)
                }
            )

            let data=await response.json()

            this.message=data.message

            if(response.ok){
                this.$router.push("/company")
            }

        }

    }

}

</script>