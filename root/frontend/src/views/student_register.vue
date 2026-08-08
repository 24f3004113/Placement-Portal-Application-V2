<template>

<h2>Student Registration</h2>

<form @submit.prevent="register">

    <label>Name</label>
    <input type="text" placeholder="Enter your Name" v-model="form.name" required>
    <br><br>

    <label>Email</label>
    <input type="email" placeholder="Enter your Email" v-model="form.email" required>
    <br><br>

    <label>Password</label>
    <input type="password" placeholder="Create Password" v-model="form.password" required>
    <br><br>

    <label>Phone Number</label>
    <input type="text" placeholder="Enter your Phone Number" v-model="form.phone" required>
    <br><br>

    <label>Course</label>
    <input type="text" placeholder="Enter Studied Course" v-model="form.course" required>
    <br><br>

    <label>CGPA</label>
    <input type="number" step="0.01" placeholder="Enter your CGPA" v-model="form.cgpa" required>
    <br><br>

    <label>Graduation Year</label>
    <input type="number" placeholder="Enter your Graduation Year" v-model="form.graduation_year" required>
    <br><br>

    <label>Skills</label>
    <input type="text" placeholder="List your Skills" v-model="form.skills">
    <br><br>

    <button type="submit">Register</button>

</form>

<br>

<p>{{ message }}</p>

</template>

<script>

export default{

    data(){

        return{
            from:{
                email:"",
                password:"",
                name:"",
                phone:"",
                course:"",
                cgpa:"",
                graduation_year:"",
                skills:""
            },
            message:""
        }

    },

    methods:{

        async register(){

            let response=await fetch("http://127.0.0.1:5000/student/register",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(this.form)

            })

            let data=await response.json()

            this.message=data.message

        }

    }

}

</script>