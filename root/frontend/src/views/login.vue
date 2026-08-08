<template>

<h2>Placement Portal</h2>

<form @submit.prevent="login">

<label>Email</label>
<input type="email" placeholder="Enter your Email" v-model="email" required>

<br><br>

<label>Password</label>
<input type="password" placeholder="Enter your Password" v-model="password" required>

<br><br>

<button type="submit">Login</button>

</form>

<br>

<button @click="$router.push('/student/register')">Student Register</button>
<button @click="$router.push('/company/register')">Company Register</button>

<br><br>

<p>{{ message }}</p>

</template>

<script>

export default{

    data(){

        return{

            email:"",
            password:"",
            message:""

        }

    },

    methods:{

        async login(){

            let response=await fetch("http://127.0.0.1:5000/login",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                credentials:"include",

                body:JSON.stringify({

                    email:this.email,
                    password:this.password

                })

            })

            let data=await response.json()

            localStorage.setItem("token", data.data.access_token)

            this.message = data.message



            if(response.ok){

                if(data.data.role=="admin")
                    this.$router.push("/admin")

                else if(data.data.role=="company")
                    this.$router.push("/company")

                else if(data.data.role=="student")
                    this.$router.push("/student")

            }

        }

    }

}

</script>