<template>

 <div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <h2 class="text-center">Create Placement Drive</h2>

            <form @submit.prevent="createDrive">

                <div class="mb-3">
                    <label class="form-label">Job Title</label>
                    <input type="text" class="form-control" placeholder="Job Title"
                        v-model="form.job_title" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" placeholder="Description"
                        v-model="form.description" required></textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label">Required Courses </label>
                    <input type="text" class="form-control" placeholder="Course"
                        v-model="form.course" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Required Minimum CGPA </label>
                    <input type="number" step="0.01" class="form-control"
                        placeholder="Minimum CGPA" v-model="form.min_cgpa" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Required Graduation Year</label>
                    <input type="number" class="form-control"
                        placeholder="Graduation Year" v-model="form.graduation_year" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Offering Salary</label>
                    <input type="number" class="form-control"
                        placeholder="Salary" v-model="form.salary" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Application Deadline</label>
                    <input type="date" class="form-control"
                        v-model="form.application_deadline" required>
                </div>

                <div class="text-center">
                    <button type="submit" class="bg-success btn shadow text-white me-2">
                        Create Drive
                    </button>
                    <button type="button" class="btn btn-secondary"
                        @click="$router.back()">Cancel</button>
                </div>

            </form>

            <p class="text-center mt-3">{{ message }}</p>

            <div class="text-center mt-3">
                <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>
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
                application_deadline: ""
            },
            message: ""
        }

    },

    methods: {

        async createDrive() {

            let response = await fetch(
                "http://localhost:5000/company/create_drive",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token")
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

            if (response.ok) {
                this.$router.push("/company")
            }

        }

    }

}

</script>