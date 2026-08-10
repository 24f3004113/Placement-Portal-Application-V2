<template>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <h2 class="text-center">Company Registration</h2>

                <form @submit.prevent="register" class="form-control">

                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" v-model="form.email" class="form-control" placeholder="Enter your Email"
                            required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" v-model="form.password" class="form-control"
                            placeholder="Create your Password" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Company Name</label>
                        <input type="text" v-model="form.company_name" class="form-control"
                            placeholder="Enter Company Name" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Industry</label>
                        <input type="text" v-model="form.industry" class="form-control"
                            placeholder="Enter Company's Industry" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Location</label>
                        <input type="text" v-model="form.location" class="form-control"
                            placeholder="Enter Company Location" required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">HR Contact</label>
                        <input type="text" v-model="form.hr_contact" class="form-control" placeholder="Enter HR Contact"
                            required>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Website</label>
                        <input type="text" v-model="form.website" class="form-control"
                            placeholder="Enter Company's Website">
                    </div>

                    <div class="text-center">
                        <button type="submit" class="bg-success btn shadow text-white">
                            Register
                        </button>
                    </div>

                </form>

                <p class="text-center mt-3">{{ message }}</p>

                <div class="text-center">
                    <button class="btn btn-primary" @click="$router.push('/')">
                        Already have an account? Login
                    </button>
                </div>

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
                password: "",
                company_name: "",
                industry: "",
                location: "",
                hr_contact: "",
                website: ""
            },

            message: ""
        }
    },

    methods: {

        async register() {

            let response = await fetch(
                "http://localhost:5000/company/register",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(this.form)
                }
            )

            let data = await response.json()

            this.message = data.message

            alert(data.message)

            if (response.ok) {
                this.$router.push("/")
            }
        }

    }

}

</script>