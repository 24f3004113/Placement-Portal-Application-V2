<template>

<h2>Edit Placement Drive</h2>

<form @submit.prevent="updateDrive">

<label>Job Title</label>
<input type="text" v-model="form.job_title" required>
<br><br>

<label>Description</label>
<textarea v-model="form.description" required></textarea>
<br><br>

<label>Course</label>
<input type="text" v-model="form.course" required>
<br><br>

<label>Minimum CGPA</label>
<input type="number" step="0.01" v-model="form.min_cgpa" required>
<br><br>

<label>Graduation Year</label>
<input type="number" v-model="form.graduation_year" required>
<br><br>

<label>Salary</label>
<input type="number" v-model="form.salary" required>
<br><br>

<label>Application Deadline</label>
<input type="date" v-model="form.application_deadline" required>
<br><br>

<label>Status</label>
<select v-model="form.status" required>
    <option value="Open">Open</option>
    <option value="Closed">Closed</option>
</select>
<br><br>

<button type="submit">Update Drive</button>
<button type="button" @click="$router.back()">Cancel</button>

</form>

<p>{{ message }}</p>

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
                "http://127.0.0.1:5000/company/drive/" +
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

            if (response.ok)
                this.form = data
            else
                this.message = data.message

        },

        async updateDrive() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/edit_drive/" +
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