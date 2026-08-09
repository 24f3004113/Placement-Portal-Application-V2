<template>

    <h2>Company Registration</h2>

    <form @submit.prevent="register">

        <label>Email</label>
        <input type="email" v-model="form.email" placeholder="Enter your Email" required>
        <br><br>

        <label>Password</label>
        <input type="password" v-model="form.password" placeholder="Create your Password" required>
        <br><br>

        <label>Company Name</label>
        <input type="text" v-model="form.company_name" placeholder="Enter Company Name" required>
        <br><br>

        <label>Industry</label>
        <input type="text" v-model="form.industry" placeholder="Enter Company's Industry" required>
        <br><br>

        <label>Location</label>
        <input type="text" v-model="form.location" placeholder="Enter Company Location" required>
        <br><br>

        <label>HR Contact</label>
        <input type="text" v-model="form.hr_contact" placeholder="Enter HR Contact" required>
        <br><br>

        <label>Website</label>
        <input type="text" v-model="form.website" placeholder="Enter Company's Website">
        <br><br>

        <button type="submit">Register</button>

    </form>

    <p>{{ message }}</p>

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
                "http://127.0.0.1:5000/company/register",
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