<template>

<h2>Company Registration</h2>

<input type="email" placeholder="Enter your Email" v-model="email">
<br><br>

<input type="password" placeholder="Create your Password" v-model="password">
<br><br>

<input type="text" placeholder="Enter Company Name" v-model="company_name">
<br><br>

<input type="text" placeholder="Enter Company's Industry" v-model="industry">
<br><br>

<input type="text" placeholder="Enter Company Location" v-model="location">
<br><br>

<input type="text" placeholder="Enter HR Contact" v-model="hr_contact">
<br><br>

<input type="text" placeholder="Enter Company's Website" v-model="website">
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
            company_name:"",
            industry:"",
            location:"",
            hr_contact:"",
            website:"",
            message:""

        }

    },

    methods:{

        async register(){

            let response=await fetch("http://127.0.0.1:5000/company/register",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    email:this.email,
                    password:this.password,
                    company_name:this.company_name,
                    industry:this.industry,
                    location:this.location,
                    hr_contact:this.hr_contact,
                    website:this.website

                })

            })

            let data=await response.json()

            this.message=data.message

        }

    }

}

</script>