<template>

    <h2 class="text-center">Application History</h2>

    <div class="row justify-content-center">
        <div class="col-md-6">
            <table class="table table-striped  table-bordered table-hover border-dark ">

                <tbody>

                    <tr>
                        <th>Company</th>
                        <th>Job Title</th>
                        <th>Status</th>
                        <th>Feedback</th>
                        <th>Updated At</th>
                    </tr>

                    <tr v-for="h in history" :key="h.id">

                        <td>{{ h.company }}</td>
                        <td>{{ h.job_title }}</td>
                        <td>{{ h.status }}</td>
                        <td>{{ h.feedback }}</td>
                        <td>{{ h.updated_at }}</td>

                    </tr>

                </tbody>

            </table>
        </div>
    </div>

    <p class="text-center">{{ message }}</p>

    <div class="text-center mt-3">
        <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>

        <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
    </div>

</template>

<script>

export default {

    data() {
        return {
            history: [],
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://localhost:5000/student/history",
            {
                headers: {
                    "Authorization":
                        "Bearer " + localStorage.getItem("token")
                },
                credentials: "include"
            }
        )

        let data = await response.json()

        if (data.msg == "Token has expired") {
            alert("Session expired. Please login again.")
            localStorage.removeItem("token")
            this.$router.push("/")
            return
        }

        if (response.ok)
            this.history = data
        else
            this.message = data.message || data.msg
    }

}

</script>