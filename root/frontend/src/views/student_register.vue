<template>

<h2>Student Registration</h2>

<input type="text" placeholder="Enter your Name" v-model="name">
<br><br>

<input type="email" placeholder="Enter your Email" v-model="email">
<br><br>

<input type="password" placeholder="Create Password" v-model="password">
<br><br>

<input type="text" placeholder="Enter your Phone Number" v-model="phone">
<br><br>

<input type="text" placeholder="Enter Studied Course" v-model="course">
<br><br>

<input type="number" placeholder="Ente your CGPA" v-model="cgpa">
<br><br>

<input type="number" placeholder="Enter your Graduation Year" v-model="graduation_year">
<br><br>

<input type="text" placeholder="List your Skills" v-model="skills">
<br><br>

<button @click="register">Register</button>

<br><br>

<p>{{message}}</p>

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