<template>

<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <h2 class="text-center">Edit Placement Drive</h2>

            <form @submit.prevent="updateDrive">

                <div class="mb-3">
                    <label class="form-label">Job Title</label>
                    <input type="text" v-model="form.job_title"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea v-model="form.description"
                        class="form-control" required></textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label">Course</label>
                    <input type="text" v-model="form.course"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Minimum CGPA</label>
                    <input type="number" step="0.01" v-model="form.min_cgpa"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Graduation Year</label>
                    <input type="number" v-model="form.graduation_year"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Salary</label>
                    <input type="number" v-model="form.salary"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Application Deadline</label>
                    <input type="date" v-model="form.application_deadline"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Status</label>
                    <select v-model="form.status" class="form-select" required>
                        <option value="Open">Open</option>
                        <option value="Closed">Closed</option>
                    </select>
                </div>

                <div class="text-center">
                    <button type="submit" class="bg-success btn shadow text-white me-2">
                        Update Drive
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
                job_title: "",
                description: "",
                course: "",
                min_cgpa: "",
                graduation_year: "",
                salary: "",
                application_deadline: "",
                status: ""
            },
            message: ""
        }

    },

    methods: {

        async getDrive() {

            let response = await fetch(
                "http://localhost:5000/company/drive/" +
                this.$route.params.did,
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
                this.form = data
            else
                this.message = data.message

        },

        async updateDrive() {

            let response = await fetch(
                "http://localhost:5000/company/edit_drive/" +
                this.$route.params.did,
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
        this.getDrive()
    }

}

</script>