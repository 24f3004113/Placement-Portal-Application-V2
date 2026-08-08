<template>

<h2>Update Company Profile</h2>

<form @submit.prevent="updateProfile">

<label>Email</label>
<input type="email" v-model="form.email" required>
<br><br>

<label>Password</label>
<input type="password" v-model="form.password" placeholder="Enter new password">
<br><br>

<label>Company Name</label>
<input type="text" v-model="form.company_name" required>
<br><br>

<label>Industry</label>
<input type="text" v-model="form.industry" required>
<br><br>

<label>Location</label>
<input type="text" v-model="form.location" required>
<br><br>

<label>HR Contact</label>
<input type="text" v-model="form.hr_contact" required>
<br><br>

<label>Website</label>
<input type="text" v-model="form.website">
<br><br>

<button type="submit">Update Profile</button>
<button type="button" @click="$router.back()">Cancel</button>

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

        async getProfile() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/profile",
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if (response.ok)
                this.form = { ...this.form, ...data }
            else
                this.message = data.message

        },

        async updateProfile() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/profile/update",
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include",
                    body: JSON.stringify(this.form)
                }
            )

            let data = await response.json()

            this.message = data.message

            if (response.ok)
                this.$router.push("/company")

        }

    },

    mounted() {
        this.getProfile()
    }

}

</script>