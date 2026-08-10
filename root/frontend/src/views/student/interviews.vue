<template>
<div class="container my-5 shadow p-2">
    <h2 class="text-center">My Interviews</h2>

    <div class="table-responsive-md">
        <table class="table table-striped table-bordered table-hover">
            <tbody>
                <tr>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Mode</th>
                    <th>Link</th>
                    <th>Location</th>
                    <th>Remarks</th>
                </tr>

                <tr v-for="i in interviews" :key="i.iid">
                    <td>{{ i.company }}</td>
                    <td>{{ i.job_title }}</td>
                    <td>{{ i.date }}</td>
                    <td>{{ i.time }}</td>
                    <td>{{ i.mode }}</td>

                    <td>
                        <a v-if="i.link"
                            :href="i.link.startsWith('http') ? i.link : 'https://' + i.link"
                            target="_blank">
                            Join Interview
                        </a>
                        <span v-else>N/A</span>
                    </td>

                    <td>{{ i.location || "N/A" }}</td>
                    <td>{{ i.remarks || "N/A" }}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <p class="text-center">{{ message }}</p>

    <div class="text-center mt-3">
        <button class="btn btn-secondary me-2"
            @click="$router.back()">Back</button>

        <button class="bg-danger btn shadow text-white"
            @click="$router.push('/logout')">Logout</button>
    </div>
</div>

</template>

<script>

export default {

    data() {
        return {
            interviews: [],
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://localhost:5000/student/interviews",
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
            this.interviews = data
        else
            this.message = data.message || data.msg
    }

}

</script>