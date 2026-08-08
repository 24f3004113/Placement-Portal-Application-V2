<template>

<h2>Create Placement Drive</h2>

<form @submit.prevent="createDrive">

<input type="text" placeholder="Job Title" v-model="form.job_title" required>

<textarea placeholder="Description" v-model="form.description" required></textarea>

<input type="text" placeholder="Course" v-model="form.course" required>

<input type="number"  placeholder="Minimum CGPA" v-model="form.min_cgpa" required>

<input type="number" placeholder="Graduation Year" v-model="form.graduation_year" required>

<input type="number" placeholder="Salary" v-model="form.salary" required>

<input type="date" v-model="form.application_deadline" required>

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