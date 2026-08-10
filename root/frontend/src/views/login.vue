<template>


<h2 class="text-center">Placement Portal</h2>

<h3 class="text-center"> Login </h3>

<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">

            <form @submit.prevent="login" class="form-control">
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" class="form-control" placeholder="Email"
                        v-model="form.email" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-control" placeholder="Password"
                        v-model="form.password" required>
                </div>

                <div class="text-center">
                    <button type="submit" class="bg-success btn shadow text-white">Login</button>
                </div>
            </form>

            <div class="text-center mt-3">
                <button class="btn btn-primary me-2"
                    @click="$router.push('/student/register')">Student Register</button>
                <button class="btn btn-primary"
                    @click="$router.push('/company/register')">Company Register</button>
            </div>

            <p class="text-center mt-3">{{ message }}</p>

        </div>
    </div>
</div>

</template>

<script>

export default {

    data() {

        return {
            form: {
                email: "",
                password: ""
            },
            message: ""

        }

    },

    methods: {

        async login() {

            let response = await fetch("http://localhost:5000/login", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                credentials: "include",

                body: JSON.stringify(this.form)

            })

            let data = await response.json()

            if (!response.ok) {
                alert(data.message)
                this.message = data.message || data.msg
                return
            }

            localStorage.setItem("token", data.data.access_token)

            this.message = data.message




            if (response.ok) {

                if (data.data.role == "admin")
                    this.$router.push("/admin")

                else if (data.data.role == "company")
                    this.$router.push("/company")

                else if (data.data.role == "student")
                    this.$router.push("/student")

            }

        }

    }

}

</script>