<template>

<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">

            <h2 class="text-center">Update Company Profile</h2>

            <form @submit.prevent="updateProfile" class="form-control">

                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" v-model="form.email"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input type="password" v-model="form.password"
                        class="form-control" placeholder="Enter new password">
                </div>

                <div class="mb-3">
                    <label class="form-label">Company Name</label>
                    <input type="text" v-model="form.company_name"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Industry</label>
                    <input type="text" v-model="form.industry"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Location</label>
                    <input type="text" v-model="form.location"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">HR Contact</label>
                    <input type="text" v-model="form.hr_contact"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Website</label>
                    <input type="text" v-model="form.website"
                        class="form-control">
                </div>

                <div class="text-center">
                    <button type="submit"
                        class="bg-success btn shadow text-white me-2">
                        Update Profile
                    </button>

                    <button type="button" class="btn btn-secondary"
                        @click="$router.back()">Cancel</button>
                </div>

            </form>

            <p class="text-center mt-3">{{ message }}</p>

            <div class="text-center mt-3">
                <button class="btn btn-secondary me-2"
                    @click="$router.back()">Back</button>

                <button class="bg-danger btn shadow text-white"
                    @click="$router.push('/logout')">Logout</button>
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

        async getProfile() {

            let response = await fetch(
                "http://localhost:5000/company/profile",
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

            if (response.ok)
                this.form = { ...this.form, ...data }
            else
                this.message = data.message

        },

        async updateProfile() {

            let response = await fetch(
                "http://localhost:5000/company/profile/update",
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

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

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