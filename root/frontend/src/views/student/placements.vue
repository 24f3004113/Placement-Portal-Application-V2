<template>
    <div class="container mt-4">
        <h2 class="text-center">My Placement</h2>

        <div class="row justify-content-center">
            <div class="col-md-6">
                <table class="table table-striped table-bordered table-hover border-dark">
                    <tbody>
                        <tr>
                            <th>Company</th>
                            <th>Position</th>
                            <th>Salary</th>
                            <th>Joining Date</th>
                        </tr>

                        <tr v-for="p in placements" :key="p.pid">
                            <td>{{ p.company }}</td>
                            <td>{{ p.position }}</td>
                            <td>{{ p.salary }}</td>
                            <td>{{ p.joining_date }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div class="text-center mt-3">
        <button class="btn btn-secondary me-2"
            @click="$router.back()">Back</button>

        <button class="bg-danger btn shadow text-white"
            @click="$router.push('/logout')">Logout</button>
    </div>


</template>

<script>

export default {

    data() {
        return {
            placements: [],
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://localhost:5000/student/placements",
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
            this.placements = data
        else
            this.message = data.message || data.msg

    }

}

</script>