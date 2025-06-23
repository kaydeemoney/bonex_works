
@app.route("/user_withdrawal_confirmation", methods=['GET', 'POST'])
@login_required
def user_withdrawal_confirmation():
    email=session.get('email')
    profile_picture=session.get('profile_picture')
    if request.method == 'POST':
        if request.form['action'] == 'confirm':
            withdraw = Withdrawal(
                user_id=request.form['user_id'],
                amount_deposited=request.form['amount_deposited'],
                senders_wallet_address=request.form['senders_wallet_address'],
                senders_wallet_network=request.form['senders_wallet_network'],
                estimated_time_of_sending=request.form['estimated_time_of_sending'],
                comment=request.form.get('comment', ''),
                status=0
            )

            transaction_copy= Transaction(user_id=request.form['user_id'],
                                          type="Deposit", amount=request.form['amount_deposited'],
                                          status="Pending",
                                          description=request.form.get('comment', ''))
            
            db.session.add(deposit)
            db.session.add(transaction_copy)
            db.session.commit()
            flash("✅ Deposit successfully confirmed and submitted. Awaiting admin review.", "success")
            return redirect(url_for('deposit_success'))

        elif request.form['action'] == 'reject':
            flash("❌ Deposit request was cancelled.", "info")
            return redirect(url_for('deposit_cancelled'))

    # GET request
    user_id = request.args.get('user_id')
    user=User.query.filter_by(user_id=user_id).first()
    amount_deposited = request.args.get('amount_deposited')
    senders_wallet_address = request.args.get('senders_wallet_address')
    senders_wallet_network = request.args.get('senders_wallet_network')
    estimated_time_of_sending = request.args.get('estimated_time_of_sending')
    comment = request.args.get('comment')
    status = request.args.get('status')



    reciever_address_wallet = AdminWalletAddress.query.filter_by(network=senders_wallet_network).first().address

    reciever_address = reciever_address_wallet if reciever_address_wallet else None
    if not reciever_address:
        flash("Invalid wallet network selected.", "danger")
        return redirect(url_for('deposit'))
    return render_template('user_deposit_confirmation.html',
                           user_id=user_id, user=user, profile_picture=profile_picture,
                           amount_deposited=amount_deposited,
                           senders_wallet_address=senders_wallet_address,
                           senders_wallet_network=senders_wallet_network,
                           estimated_time_of_sending=estimated_time_of_sending,
                           comment=comment,
                           status=status,
                           reciever_address=reciever_address)

