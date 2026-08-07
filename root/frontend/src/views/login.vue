<template>

<h2>Placement Portal</h2>

<input type="email" placeholder="Email" v-model="email">

<br><br>

<input type="password" placeholder="Password" v-model="password">

<br><br>

<button @click="login">Login</button>

<button @click="$router.push('/student/register')">Student Register</button>

<button @click="$router.push('/company/register')">Company Register</button>

<br><br>

<p>{{message}}</p>

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