<template>

<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">

            <h2 class="text-center">Edit Profile</h2>

            <form @submit.prevent="updateProfile">

                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input type="text" v-model="form.name"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" v-model="form.email"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input type="password" v-model="form.password"
                        class="form-control">
                </div>

                <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input type="text" v-model="form.phone"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Course</label>
                    <input type="text" v-model="form.course"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">CGPA</label>
                    <input type="number" step="0.01" v-model="form.cgpa"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Graduation Year</label>
                    <input type="number" v-model="form.graduation_year"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Skills</label>
                    <textarea v-model="form.skills"
                        class="form-control"></textarea>
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
                name: "",
                email: "",
                password: "",
                phone: "",
                course: "",
                cgpa: "",
                graduation_year: "",
                skills: ""
            },

            message: ""
        }
    },

    methods: {

        async getProfile() {

            let response = await fetch(
                "http://localhost:5000/student/profile",
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

            if (response.ok) {

                this.form.name = data.name
                this.form.email = data.email
                this.form.phone = data.phone
                this.form.course = data.course
                this.form.cgpa = data.cgpa
                this.form.graduation_year = data.graduation_year
                this.form.skills = data.skills

            } else {

                this.message = data.message

            }

        },

        async updateProfile() {

            let data = {
                name: this.form.name,
                email: this.form.email,
                phone: this.form.phone,
                course: this.form.course,
                cgpa: this.form.cgpa,
                graduation_year: this.form.graduation_year,
                skills: this.form.skills
            }

            if (this.form.password)
                data.password = this.form.password

            let response = await fetch(
                "http://localhost:5000/student/profile/update",
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json",
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },

                    credentials: "include",

                    body: JSON.stringify(data)
                }
            )

            let result = await response.json()

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }


            this.message = result.message

            if (response.ok) {
                alert(result.message)
                this.$router.push("/student")
            } else {
                alert(result.message)
            }

        }

    },

    mounted() {
        this.getProfile()
    }

}

</script>