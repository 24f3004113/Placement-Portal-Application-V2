<template>

<h2>Company Registration</h2>

<form @submit.prevent="register">

    <label>Email</label>
    <input type="email" placeholder="Enter your Email" v-model="form.email" required>
    <br><br>

    <label>Password</label>
    <input type="password" placeholder="Create your Password" v-model="form.password" required>
    <br><br>

    <label>Company Name</label>
    <input type="text" placeholder="Enter Company Name" v-model="form.company_name" required>
    <br><br>

    <label>Industry</label>
    <input type="text" placeholder="Enter Company's Industry" v-model="form.industry" required>
    <br><br>

    <label>Location</label>
    <input type="text" placeholder="Enter Company Location" v-model="form.location" required>
    <br><br>

    <label>HR Contact</label>
    <input type="text" placeholder="Enter HR Contact" v-model="form.hr_contact" required>
    <br><br>

    <label>Website</label>
    <input type="text" placeholder="Enter Company's Website" v-model="form.website">
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
            form:{
                email:"",
                password:"",
                company_name:"",
                industry:"",
                location:"",
                hr_contact:"",
                website:""
            },
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