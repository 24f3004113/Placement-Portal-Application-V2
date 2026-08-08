<template>

<h2>Student Registration</h2>

<form @submit.prevent="register">

    <label>Name</label>
    <input type="text" placeholder="Enter your Name" v-model="name" required>
    <br><br>

    <label>Email</label>
    <input type="email" placeholder="Enter your Email" v-model="email" required>
    <br><br>

    <label>Password</label>
    <input type="password" placeholder="Create Password" v-model="password" required>
    <br><br>

    <label>Phone Number</label>
    <input type="text" placeholder="Enter your Phone Number" v-model="phone" required>
    <br><br>

    <label>Course</label>
    <input type="text" placeholder="Enter Studied Course" v-model="course" required>
    <br><br>

    <label>CGPA</label>
    <input type="number" step="0.01" placeholder="Enter your CGPA" v-model="cgpa" required>
    <br><br>

    <label>Graduation Year</label>
    <input type="number" placeholder="Enter your Graduation Year" v-model="graduation_year" required>
    <br><br>

    <label>Skills</label>
    <input type="text" placeholder="List your Skills" v-model="skills">
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

            email:"",
            password:"",
            name:"",
            phone:"",
            course:"",
            cgpa:"",
            graduation_year:"",
            skills:"",
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

                body:JSON.stringify({

                    email:this.email,
                    password:this.password,
                    name:this.name,
                    phone:this.phone,
                    course:this.course,
                    cgpa:this.cgpa,
                    graduation_year:this.graduation_year,
                    skills:this.skills

                })

            })

            let data=await response.json()

            this.message=data.message

        }

    }

}

</script>