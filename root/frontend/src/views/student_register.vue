<template>

<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <h2 class="text-center">Student Registration</h2>

            <form @submit.prevent="register" class="form-control">

                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input type="text" v-model="form.name" class="form-control"
                        placeholder="Enter your Name" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" v-model="form.email" class="form-control"
                        placeholder="Enter your Email" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input type="password" v-model="form.password" class="form-control"
                        placeholder="Create Password" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Phone Number</label>
                    <input type="text" v-model="form.phone" class="form-control"
                        placeholder="Enter your Phone Number" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Course</label>
                    <input type="text" v-model="form.course" class="form-control"
                        placeholder="Enter Studied Course" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">CGPA</label>
                    <input type="number" step="0.01" v-model="form.cgpa" class="form-control"
                        placeholder="Enter your CGPA" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Graduation Year</label>
                    <input type="number" v-model="form.graduation_year" class="form-control"
                        placeholder="Enter your Graduation Year" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Skills</label>
                    <input type="text" v-model="form.skills" class="form-control"
                        placeholder="List your Skills">
                </div>

                <div class="text-center">
                    <button type="submit" class="bg-success btn shadow text-white">
                        Register
                    </button>
                </div>

            </form>

            <p class="text-center mt-3">{{ message }}</p>

            <div class="text-center">
                <button class="btn btn-primary"
                    @click="$router.push('/')">
                    Back to Login
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

        async register() {

            let response = await fetch("http://localhost:5000/student/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.form)
            })

            let data = await response.json()

            this.message = data.message

            if (response.ok) {
                this.$router.push("/")
            }
        }

    }

}

</script>